from argparse import ArgumentParser, Namespace, SUPPRESS
import copy
from collections import defaultdict, Mapping
import importlib
import json
import re
from typing import Dict, Iterable, List, Optional, Set, Tuple, Union
import warnings
import yaml

from pampy import match, MatchError

from paranormal.params import *
from paranormal.units import convert_to_si_units, unconvert_si_units

__all__ = ['Params', 'to_json_serializable_dict', 'from_json_serializable_dict', 'to_yaml_file',
           'from_yaml_file', 'create_parser_and_parse_args', 'to_argparse', 'from_parsed_args',
           'get_param_unit', 'merge_param_classes', 'append_params_attributes']


####################
# Params Interface #
####################


class Params(Mapping):
    """
    Base class for Params

    Supports:
    1. ** operation
    2 * operation (iterate through param names)

    Does Not Support:
    1. Non-direct inheritance (inheriting from a class that inherits from Params)

    Example Use Case:

    Inherit from this class and populate with Param classes from paranormal.params
    ```
    class A(Params):
        g = GeomspaceParam(help='test', default=[0, 100, 20])
        i = IntParam(help='my favorite int', required=True, choices=[1,2,3])
    ```
    """
    def __init__(self, **kwargs):
        cls = type(self)
        if cls not in Params.__subclasses__():
            raise NotImplementedError('Behavior is undefined for classes that do not directly '
                                      'inherit from Params.')
        _copy_nested_classes(self)
        for key, value in kwargs.items():
            if not key in cls.__dict__:
                raise KeyError(f'{cls.__name__} does not take {key} as an argument')
            setattr(self, key, value)
        _check_for_required_arguments(cls, kwargs)
        _ensure_properties_are_working(self)

    def __iter__(self):
        valid_keys = [k for k in self.__class__.__dict__.keys() if not k.startswith('_')]
        for key in valid_keys:
            yield key

    def __len__(self):
        return len(list(self.__iter__()))

    def __getitem__(self, item):
        return getattr(self, item)

    def __eq__(self, other) -> bool:
        return json.loads(json.dumps(to_json_serializable_dict(self))) == \
               json.loads(json.dumps(to_json_serializable_dict(other)))

    def unit_set(self, param_name: str, value: Union[float, int, Iterable]) -> None:
        """
        Set the parameter from a value that's in the param units specified in the Params class
        definition

        Ex.
        ```
        class A(Params):
            f = FloatParam(help='float', unit='ns')

        a = A()
        a.unit_set('a', 5)
        print(a.f)  # prints 5e-9
        ```

        :param param_name: The parameter name to set
        :param value: The new value in SI units
        """
        param = type(self).__dict__.get(param_name)
        expanded_units = _expand_param_units(param)
        if expanded_units is not None:
            values = [convert_to_si_units(v, u) for v, u in zip(value, expanded_units)]
            setattr(self, param_name, values)
        else:
            unit = get_param_unit(type(self), param_name)
            if not isinstance(value, Iterable):
                setattr(self, param_name, convert_to_si_units(value, unit))
            else:
                # need to keep parameter type
                val_type = type(value)
                setattr(self, param_name, val_type([convert_to_si_units(v, unit) for v in value]))

    def unit_update(self, **kwargs) -> None:
        """
        Set parameters from multiple values using units specified in the Params class definition

        :param kwargs: parameter names and values to set
        """
        for k, v in kwargs.items():
            self.unit_set(k, v)

    def update(self, **kwargs) -> None:
        """
        Set multiple parameters at once.

        :param kwargs: parameter names and values to set
        """
        for k, v in kwargs.items():
            setattr(self, k, v)


def get_param_unit(cls: type(Params), param_name: str) -> str:
    """
    Get the unit of a param
    """
    return getattr(cls.__dict__.get(param_name), 'unit', None)


def _check_for_required_arguments(cls: type(Params), kwargs: dict) -> None:
    """
    Make sure the arguments required by Params class or subclass exist in the kwargs dictionary
    used to instantiate the class
    """
    required_but_not_provided = []
    for k, v in cls.__dict__.items():
        if k.startswith('_') or not isinstance(v, BaseDescriptor):
            continue
        elif getattr(v, 'required', None) and not k in kwargs:
            required_but_not_provided.append(k)
    if required_but_not_provided != []:
        raise KeyError(f'{required_but_not_provided} are required arguments to instantiate '
                       f'{cls.__name__}')


def _ensure_properties_are_working(params: Params) -> None:
    """
    Evaluate the properties within a class to make sure they work based on the attributes
    """
    for k, v in params.items():
        if isinstance(v, property):
            getattr(params, k)


def _copy_nested_classes(params: Params):
    """
    Deepcopy and set any nested params classes to make sure users cannot mutate the nested classes.
    This function will mutate the passed in params class
    """
    for k, v in type(params).__dict__.items():
        if isinstance(v, Params):
            setattr(params, k, copy.deepcopy(v))


#################
# Serialization #
#################


def to_json_serializable_dict(params: Params,
                              *,
                              include_defaults: bool = True,
                              include_hidden_params: bool = False,
                              params_to_omit: Optional[Set[str]] = None) -> dict:

    """
    Convert Params class to a json serializable dictionary
    :param params: Params class to convert
    :param include_defaults: Whether or not to include the param attribute default values if the
        values haven't been set yet
    :param include_hidden_params: Whether or not to include params that start with _
    :param params_to_omit: Params to set to None when serializing the params class
    :return A dictionary that's json serializable
    """
    retval = {}
    for k, v in type(params).__dict__.items():
        if params_to_omit is not None and k in params_to_omit:
            continue
        if (
                (not k.startswith('_') or not getattr(v, 'hide', False) or include_hidden_params) and
                (include_defaults or k in params.__dict__)
        ):
            if isinstance(v, BaseDescriptor):
                retval[k] = v.to_json(params)
            elif isinstance(v, Params):
                nested_params = params.__dict__.get(k, v)
                _params_to_omit = _get_omitted_params(v)
                if _get_omitted_params(nested_params) - _params_to_omit != set():
                    warnings.warn('Params can only be marked as omitted inside the class definition'
                                  f' - ({_get_omitted_params(nested_params) - _params_to_omit})  '
                                  'will not be omitted.')
                retval[k] = to_json_serializable_dict(nested_params,
                                                      include_defaults=include_defaults,
                                                      include_hidden_params=include_hidden_params,
                                                      params_to_omit=_params_to_omit)
    retval['_type'] = params.__class__.__name__
    retval['_module'] = params.__class__.__module__
    return retval


def from_json_serializable_dict(dictionary: dict,
                                params_to_omit: Optional[Set[str]] = None) -> Params:
    """
    Convert from a json serializable dictionary to a Params class
    :param dictionary: a dictionary in the format returned by to_json_serializable_dict to convert
        back to a Params class
    :param params_to_omit: Params to set to None when de-serializing the dictionary
    :return The Params class
    """
    temp_dictionary = copy.deepcopy(dictionary)
    try:
        cls_type = temp_dictionary.pop('_type')
        module_name = temp_dictionary.pop('_module')
        module = importlib.import_module(module_name)
        cls = getattr(module, cls_type)
    except KeyError:
        raise ValueError('Dictionary Format Not Recognized!')
    # handle case with nested params
    unraveled_dictionary = {}
    for k, v in cls.__dict__.items():
        if isinstance(v, BaseDescriptor):
            if params_to_omit is not None and k in params_to_omit:
                unraveled_dictionary[k] = None
            elif k in temp_dictionary:
                unraveled_dictionary[k] = temp_dictionary[k]
        elif isinstance(v, Params):
            _params_to_omit = _get_omitted_params(v)
            unraveled_dictionary[k] = from_json_serializable_dict(temp_dictionary[k],
                                                                  params_to_omit=_params_to_omit)
    return cls(**unraveled_dictionary)


def to_yaml_file(params: Params,
                 filename: str,
                 *,
                 include_defaults: bool = False,
                 include_hidden_params: bool = False,
                 sort_keys: bool = False):
    """
    Dump to yaml
    """
    d = to_json_serializable_dict(params, include_defaults=include_defaults,
                                  include_hidden_params=include_hidden_params)

    with open(filename, 'w') as f:
        yaml.dump(d, stream=f, sort_keys=sort_keys)


def from_yaml_file(filename: str) -> Params:
    """
    Parse from yaml
    """
    with open(filename, 'r') as f:
        params = from_json_serializable_dict(yaml.full_load(f))
    return params


#############################
# Params Class Manipulation #
#############################


def _merge_positional_params(params_list: List[Tuple[str, BaseDescriptor]]
                             ) -> Tuple[List[str], Optional[BaseDescriptor]]:
    """
    Merge positional params into a single list param and return a list of param names that were
    merged

    :param params_list: List of params (name, Param) to search through for positional params. If
        multiple positional params are found, they will be merged into a single positional
        ListParam.
    :return The positional param names in the list, the merged ListParam
    """
    if not sum([getattr(p, 'positional', False) for (_, p) in params_list]) > 1:
        return [], None
    positionals = {k: v for (k, v) in params_list
                   if getattr(v, 'positional', False)}
    # Just parse all positionals as a ListParam - we'll match them back up later in
    # _parse_positional_arguments
    positional_param = ListParam(help=', '.join(v.help for v in positionals.values()
                                                if v.help != SUPPRESS),
                                 positional=True, required=True, nargs='+')
    return list(positionals.keys()), positional_param


def merge_param_classes(*cls_list,
                        merge_positional_params: bool = True) -> type(Params):
    """
    Merge multiple Params classes into a single merged params class and return the merged class.
    Note that this will not flatten the nested classes.

    :param cls_list: A list of Params subclasses or classes to merge into a single
        Params class
    :param merge_positional_params: Whether or not to merge the positional params in the classes
    """
    if len(cls_list) == 1:
        return cls_list[0]

    class MergedParams(Params):
        __doc__ = f'A Combination of {len(cls_list)} Params Classes:\n'

    append_params_attributes(MergedParams, *cls_list)
    for params_cls in cls_list:
        MergedParams.__doc__ += f'\n\t {params_cls.__name__} - {params_cls.__doc__}'

    # resolve positional arguments:
    if merge_positional_params:
        params_to_delete, positional_param = _merge_positional_params(
            [(k, v) for k, v in MergedParams.__dict__.items() if not k.startswith('_')])
        if positional_param is None and params_to_delete == []:
            return MergedParams
        setattr(MergedParams, 'positionals', positional_param)
        positional_param.__set_name__(MergedParams, 'positionals')
        for k in params_to_delete:
            delattr(MergedParams, k)

    return MergedParams


def append_params_attributes(cls: type(Params),
                             *other_cls_list,
                             do_not_copy: Optional[List[str]] = None,
                             override_dictionary: Optional[Dict] = None) -> None:
    """
    When building a Params subclass, copy parameters from other Params subclasses using this
    function (which will mutate the Params subclass but not the classes being copied from). If
    there are parameters you do not want to copy, specify them in the do_not_copy list, and if
    you'd like to override any defaults, specify them in the override_dictionary. Any merge
    conflicts will throw an error.

    :param cls: The params subclass to copy to
    :param other_cls_list: Any number or other params subclasses to copy from
    :param do_not_copy: A list of parameters not to copy
    :param override_dictionary: A dictionary specifying any overrides to parameters (help, default,
        etc.)


    Ex.

    ```python

    class A(Params):
        i = IntParam(help='int', default=1)

    class B(Params):
        f = FloatParam(help='float', default=2.0)
        z = IntParam(help='another int')


    append_params_attributes(A, B, do_not_copy=['z'],
                            override_dictionary={'f' : {'help': 'a better float', 'default': 3.0}})
    a = A()
    print(a.f)  # prints 3.0
    print(a.z)  # throws error
    ```
    """
    for other_cls in other_cls_list:
        for k, v in other_cls.__dict__.items():
            if not (k.startswith('_') or (do_not_copy is not None and k in do_not_copy)):
                if cls.__dict__.get(k, None) is not None:
                    raise ValueError(f'Unable to append params from classes {other_cls_list} due '
                                     f'to conflicting param: {k}')
                if isinstance(v, BaseDescriptor):
                    copied_v = copy.deepcopy(v)
                    copied_v.__set_name__(cls, k)
                elif isinstance(v, Params):
                    copied_v = copy.deepcopy(v)
                elif isinstance(v, property):
                    copied_v = v
                else:
                    copied_v = copy.deepcopy(v)
                if override_dictionary is not None and k in override_dictionary:
                    for _k, _v in override_dictionary[k].items():
                        setattr(copied_v, _k, _v)
                setattr(cls, k, copied_v)


####################
# Argument Parsing #
####################


def _get_param_type(param) -> type:
    """
    Get the expected type of a param
    """
    argtype = match(param,
                    LinspaceParam, lambda x: float,
                    SpanLinspaceParam, lambda x: float,
                    ArangeParam, lambda x: float,
                    SpanArangeParam, lambda x: float,
                    GeomspaceParam, lambda x: float,
                    ListParam, lambda x: param.subtype,
                    SetParam, lambda x: param.subtype,
                    EnumParam, lambda x: str,
                    IntParam, lambda x: int,
                    FloatParam, lambda x: float,
                    BoolParam, lambda x: None,
                    StringParam, lambda x: str,
                    BaseDescriptor, lambda x: type(getattr(param, 'default', None)))
    return argtype


def _convert_type_to_regex(argtype: type) -> str:
    """
    Source of truth for getting regex strings to match different types
    """
    regex_patterns = {int: r'\b[\+-]?(?<![\.\d])\d+(?!\.\d)\b',
                      float: r'[-\+]?(?:\d+(?<!\.)\.?(?!\.)\d*|\.?\d+)(?:[eE][-\+]?\d+)?',
                      str: r'\b.*\b'}
    return regex_patterns[argtype]


def _parse_positional_arguments(list_of_positionals: List[str],
                                positional_params: Dict[str, BaseDescriptor]) -> dict:
    """
    If params have been merged together, their positional arguments will have been merged as well
    into one single ListParam. This function's job is to pair the positionals with their respective
    unmerged param classes.

    :param list_of_positionals: A list of the positional arguments from the command line arguments
    :param positional_params: The positional parameters to match the positionals to
    :return: A dictionary that maps param name to its correct value in the positionals list
    """
    if list_of_positionals is None and positional_params != {}:
        raise ValueError('No positional arguments were returned from the parser')
    elif list_of_positionals is None and positional_params == {}:
        return {}
    # first loop through combs for params that have choices specified
    copied_pos_params = copy.deepcopy(positional_params)
    copied_pos_list = copy.deepcopy(list_of_positionals)
    correctly_matched_params = {}
    params_to_delete = []
    for name, param in copied_pos_params.items():
        choices = getattr(param, 'choices', None)
        if choices is not None:
            nargs = str(getattr(param, 'nargs', 1))
            # convert to raw string to handle escape characters
            matched = [p for p in copied_pos_list
                       if re.match(r'|'.join(fr'{c}' for c in choices), p)]
            if matched == []:
                raise ValueError(f'Could not match any of the choices: {choices} in '
                                 f'positionals: {list_of_positionals} for param: {name}')
            if not nargs in ['+', '*', '?']:
                # only take the first nargs arguments
                matched = matched[:int(nargs)]
            # convert to expected type
            if getattr(param, 'nargs', None) is not None:
                correctly_matched_params[name] = [_get_param_type(param)(p) for p in matched]
            else:
                correctly_matched_params[name] = _get_param_type(param)(matched[0])
            # remove matches
            for p in matched:
                copied_pos_list.remove(p)
            params_to_delete.append(name)
    # do garbage collection at the end to avoid mutating the list we're iterating through
    for n in params_to_delete:
        del copied_pos_params[n]

    # second loop through matches to type - for nargs +, *, and ?, the behavior is greedy
    params_to_delete = []
    # first sort unmatched params by least to most restrictive type (int, float, str)

    def _type_sorter(p) -> int:
        argtype = _get_param_type(p[1])
        order = defaultdict(lambda x: 4)
        order.update({int: 1, float: 2, str: 3})
        return order[argtype]

    for name, param in sorted(copied_pos_params.items(), key=_type_sorter):
        argtype = _get_param_type(param)
        pattern = _convert_type_to_regex(argtype)
        matched = [p for p in copied_pos_list if re.match(pattern, p)]
        if matched == []:
            raise ValueError(f'Unable to find {argtype} in {list_of_positionals} for param: {name}')
        nargs = str(getattr(param, 'nargs', 1))
        if not nargs in ['+', '*', '?']:
            matched = matched[:int(nargs)]
        # convert to expected type
        if getattr(param, 'nargs', None) is not None:
            correctly_matched_params[name] = [_get_param_type(param)(p) for p in matched]
        else:
            correctly_matched_params[name] = _get_param_type(param)(matched[0])
        # remove matches
        for p in matched:
            copied_pos_list.remove(p)
        params_to_delete.append(name)
    # do garbage collection at the end to avoid mutating the list we're iterating through
    for n in params_to_delete:
        del copied_pos_params[n]

    # No third Loop
    assert copied_pos_params == {} and copied_pos_list == [], 'Unable to parse positional arguments'
    return correctly_matched_params


def _add_param_to_parser(name: str, param: BaseDescriptor, parser: ArgumentParser) -> None:
    """
    Function to add a Param like IntParam, FloatParam, etc. called <name> to a parser

    :param name: The param name
    :param param: The param to add (IntParam, FloatParam, etc.)
    :param parser: The argument parser to add the param to.
    """
    argtype = _get_param_type(param)
    if argtype == type(None):
        raise NotImplementedError(f'Argparse type not implemented '
                                  f'for {param.__class__.__name__} and default not specified')
    positional = getattr(param, 'positional', False)
    if getattr(param, 'prefix', '') != '' and not getattr(param, 'expand', False):
        raise ValueError(f'Failure with param {name}. Cannot add a prefix to a class without the'
                         f' expand kwarg set to True')
    argname = name if positional else '--' + name
    required = True if getattr(param, 'required', False) else None
    default = param.default if required is None else None
    unit = getattr(param, 'unit', None)

    # display default in units of `unit`. Unit will get added back in `from_parsed_args`
    expanded_units = _expand_param_units(param)
    if expanded_units is not None and default is not None:
        default = tuple([unconvert_si_units(d, u) for d, u in zip(default, expanded_units)])
    else:
        default = unconvert_si_units(default, unit)

    # format metavar nicely for parameters that have expanded versions but aren't expanded
    # check to see if the parameter has expanded param names
    metavar = None
    try:
        expanded_param_names = _get_expanded_param_names(param)
    except MatchError:
        expanded_param_names = []
    if not getattr(param, 'expand', False) and expanded_param_names != []:
        metavar = tuple(x.upper() for x in expanded_param_names)

    # format help nicely if default is specified and suppress is not set
    help = param.help
    if not (positional or param.help == SUPPRESS):
        if unit is not None:
            help += f' [default: {default} {unit}]'
        else:
            help += f' [default: {default}]'
    if not required and positional:
        # TODO: use nargs='*' or nargs='?' to support not-required positional arguments
        raise ValueError('Not-required positional arguments are currently not supported')
    elif positional:
        # positional arguments are required by default, and argparse complains if you specify
        # required = True
        required = None
        default = None
    action = match(param,
                   BoolParam, lambda p: 'store_true' if not p.default else 'store_false',
                   BaseDescriptor, lambda p: None)
    nargs = getattr(param, 'nargs', None)
    assert not (action is not None and nargs is not None)
    choices = match(param,
                    EnumParam, lambda x: list(x.cls.__members__.keys()),
                    BaseDescriptor, lambda x: getattr(x, 'choices', None))
    kwargs = dict(action=action, nargs=nargs, default=default, metavar=metavar,
                  type=argtype, required=required, help=help, choices=choices)
    # we delete all kwargs that are None to avoid hitting annoying action class initializations
    # such as when action is store_true and 'nargs' is in kwargs
    for kw in list(kwargs.keys()):
        if kwargs[kw] is None:
            del kwargs[kw]
    parser.add_argument(argname, **kwargs)


def _get_hidden_params(cls: Params) -> Set[str]:
    """
    Get a set of all params that are listed in __params_to_hide__
    """
    # TODO: need to recurse for doubly-nested params classes
    return set(getattr(cls, '__params_to_hide__', []))


def _get_omitted_params(params: Params) -> Set[str]:
    """
    Get a set of all params that have their value set to __omit__
    """
    return set(_k for _k in params.keys()
               if isinstance(params.__dict__.get(_k, None), str) and
               params.__dict__.get(_k, None) == '__omit__')


def _get_expanded_param_names(param: BaseDescriptor) -> List[str]:
    """
    Get bare expanded param names
    """
    return match(param,
                 SpanArangeParam, ['center', 'width', 'step'],
                 GeomspaceParam, ['start', 'stop', 'num'],
                 ArangeParam, ['start', 'stop', 'step'],
                 LinspaceParam, ['start', 'stop', 'num'],
                 SpanLinspaceParam, ['center', 'width', 'num'])


def _expand_param_name(param: BaseDescriptor) -> List[str]:
    """
    Get expanded param names

    :param param: The param to expand
    """
    if not getattr(param, 'expand', False):
        raise ValueError('Cannot expand param that does not have the expand kwarg')
    new_arg_names = _get_expanded_param_names(param)
    prefix = getattr(param, 'prefix', '')
    new_arg_names = [prefix + n for n in new_arg_names]
    return new_arg_names


def _expand_param_units(param: BaseDescriptor) -> List[Optional[str]]:
    """
    Get expanded param units

    :param param: The param to get units for
    :return: A list of the units (or None if no unit)
    """
    unit = getattr(param, 'unit', None)
    expanded_units = match(param,
                           GeomspaceParam,
                           lambda p: [unit, unit, None],
                           ArangeParam,
                           lambda p: [unit, unit, unit],
                           SpanArangeParam,
                           lambda p: [unit, unit, unit],
                           LinspaceParam,
                           lambda p: [unit, unit, None],
                           SpanLinspaceParam,
                           lambda p: [unit, unit, None],
                           BaseDescriptor, None)
    return expanded_units


def _expand_multi_arg_param(name: str, param: BaseDescriptor) -> Tuple[Tuple, Tuple, Tuple]:
    """
    Expand a parameter like GeomspaceParam or ArangeParam into seperate IntParams and FloatParams to
    parse as '--start X --stop X --num X' or '--start X --stop X --step X', etc.

    :param name: The param name
    :param param: The param to expand
    """
    new_arg_names = _expand_param_name(param)
    if getattr(param, 'positional', False):
        raise ValueError(f'Cannot expand positional {param.__class__.__name__} to {new_arg_names}')
    # expand the types
    expanded_types = match(param,
                           GeomspaceParam, [FloatParam, FloatParam, IntParam],
                           ArangeParam, [FloatParam, FloatParam, FloatParam],
                           SpanArangeParam, [FloatParam, FloatParam, FloatParam],
                           LinspaceParam, [FloatParam, FloatParam, IntParam],
                           SpanLinspaceParam, [FloatParam, FloatParam, IntParam])

    # expand the units
    expanded_units = _expand_param_units(param)

    # expand the defaults
    defaults = getattr(param, 'default', [None, None, None])
    if defaults is None:
        defaults = [None, None, None]

    # expand the choices
    choices = getattr(param, 'choices', None)
    expanded_choices = [[], [], []]
    if choices is not None:
        # transpose the choices for easy splitting but preserve type
        for c in choices:
            expanded_choices[0].append(c[0])
            expanded_choices[1].append(c[1])
            expanded_choices[2].append(c[2])

    # actually create the expanded params
    expanded_params = []
    for i, (default, argtype, u) in enumerate(zip(defaults, expanded_types, expanded_units)):
        new_param = argtype(help=param.help + ' (expanded into three arguments)',
                            default=default,
                            required=getattr(param,'required', False),
                            choices=expanded_choices[i] if choices is not None else None,
                            unit=u)
        expanded_params.append((new_arg_names[i], new_param))
    # we add the param we're expanding to the list as well to make sure the user does not pass it
    # Otherwise, it will get parsed silently, and the user will wonder what's happening
    copied_param = copy.deepcopy(param)
    setattr(copied_param, 'required', False)
    setattr(copied_param, 'help', SUPPRESS)
    setattr(copied_param, 'default', None)
    expanded_params.append((name, copied_param))
    return tuple(expanded_params)


def _extract_expanded_param(parsed_values: dict,
                            name: str,
                            param: BaseDescriptor,
                            prefix: Optional[str]) -> Optional[List]:
    """
    Convert [start, stop, num] or [start, stop, step], etc. from expanded form back into a list to
    be easily fed into the un-expanded param

    :param parsed_values: The parsed values from the command line as a dictionary (comes directly
        from the namespace)
    :param name: Original name of the param that was expanded (may have a prefix)
    :param param: The param that was expanded
    :param prefix: If the param is a nested param, there's a chance we had to append
        the enclosing class name as a prefix to deconflict arguments with the same name. See
        _create_param_name_prefix docstring for more info.
    """
    old_arg_names = [prefix + n if prefix is not None else n for n in _expand_param_name(param)]
    assert parsed_values.get(name) is None, f'param {name} was expanded! ' \
                                            f'Please provide {old_arg_names} instead'
    start_stop_x_list = [parsed_values[n] for n in old_arg_names]
    if all([x is None for x in start_stop_x_list]):
        return None
    units = _expand_param_units(param)
    si_unit_start_stop_x = [convert_to_si_units(p, u) for p, u in zip(start_stop_x_list, units)]
    return si_unit_start_stop_x


def _create_param_name_prefix(enclosing_param_name: Optional[str],
                              prefix_dictionary: Optional[Dict]) -> str:
    """
    Create a param name variant to de-conflict conflicting params

    :param enclosing_param_name: The name of the enclosing class's parameter
    :param prefix_dictionary: If the user sets __nested_prefixes__ in their Params class
        declaration, they can manually override any prefix for a nested class or specify not to use
        one by specifying None.

    Ex.
    ```
    class A(Params):
        x = LinspaceParam(expand=True, ...)

    class B(Params):
        x = LinspaceParam(expand=True, ...)

    class C(Params):
        a = A()
        b = B()
    ```
    will result in a_start, a_stop, a_num, b_start, b_stop, and b_num as command line parameters
    because there's a conflict with x in both A and B.

    The enclosing param names for x are "a" and "b" in this example.

    Ex 2.
    ```
    class A(Params):
        x = LinspaceParam(expand=True, ...)

    class B(Params):
        x = LinspaceParam(expand=True, ...)

    class C(Params):
        __nested_prefixes__ = {'a': 'ayy', 'b': None}
        a = A()
        b = B()
    ```
    will result in ayy_start, ayy_stop, ayy_num, start, stop, and num as command line
    parameters.
    """
    if prefix_dictionary is not None and enclosing_param_name is not None:
        prefix = prefix_dictionary.get(enclosing_param_name, enclosing_param_name)
        return prefix if prefix is not None else ''
    return enclosing_param_name + '_' if enclosing_param_name is not None else ''


def _flatten_cls_params(cls: type(Params),
                        use_prefix: bool = True,
                        params_to_omit: Optional[Set[str]] = None,
                        defaults_to_overwrite: Optional[Dict] = None) -> Dict:
    """
    Extract params from a Params class - Behavior is as follows:
    1. Params with names starting in _ or with the hide attribute set to True will be ignored
    2. Properties and params in the params_to_omit set will be ignored
    3. If the class contains nested params classes, those will be flattened. Any nested class
        param set to __omit__ will be omitted
    4. If use_prefix is True, a prefix (the enclosing param name) will be prepended to any nested
        class parameter names no matter what.
    5. If there are any name conflicts during flattening, those will be resolved by prepending the
        enclosing param names as prefixes if use_prefix is True.
        See _create_param_name_prefix docstring for more details
    """
    already_flat_params = {}
    for name, param in vars(cls).items():
        # ignore params are in params_to_omit
        if params_to_omit is not None and name in params_to_omit:
            continue
        # if we have an actual param
        elif isinstance(param, BaseDescriptor):
            # overwrite the parameter default value if specified
            if defaults_to_overwrite is not None and name in defaults_to_overwrite:
                param = copy.deepcopy(param)  # need to deepcopy to avoid modifying the class
                setattr(param, 'default', defaults_to_overwrite[name])
            # if the param is supposed to be expanded, then expand it
            if getattr(param, 'expand', False):
                expanded = _expand_multi_arg_param(name, param)
                if any(n in already_flat_params for (n, _) in expanded):
                    raise ValueError('Please provide prefixes for the expanded params - conflict '
                                     f'with param: {name}')
                already_flat_params.update(dict(expanded))
            else:
                already_flat_params[name] = param
        # if the param is a nested param class
        elif isinstance(param, Params):
            _params_to_omit = _get_omitted_params(param)
            _defaults_to_overwrite = param.__dict__
            flattened_nested_params = _flatten_cls_params(
                type(param),
                use_prefix=use_prefix,
                params_to_omit=_params_to_omit,
                defaults_to_overwrite=_defaults_to_overwrite)
            for n, p in flattened_nested_params.items():
                if n in already_flat_params and not use_prefix:
                    raise KeyError(f'Unable to flatten {cls.__name__} - conflict with param: {n}')
                if not use_prefix:
                    already_flat_params[n] = p
                else:
                    prefix = _create_param_name_prefix(name,
                                                       getattr(cls, '__nested_prefixes__', None))
                    name_variant = prefix + n
                    if name_variant in already_flat_params:
                        raise KeyError(
                            f'Unable to flatten {cls.__name__} - conflict with param: {n} - '
                            f'attempted to use param name: {name_variant} but failed.')
                    already_flat_params[name_variant] = p

    return already_flat_params


def _unflatten_params_cls(cls: type(Params),
                          parsed_params: dict,
                          prefix: Optional[str] = None,
                          params_to_omit: Optional[Set[str]] = None,
                          params_to_hide: Optional[Set[str]] = None) -> Params:
    """
    Recursively construct a Params class or subclass (handles nested Params classes) using values
    parsed from the command line, and apply units.

    :param cls: The Params class to create an instance of
    :param parsed_params: The params parsed from the command line
    :param prefix: The prefix for all param names
    :param params_to_omit: Params to set to None when de-serializing the parsed params dictionary
    :return: An instance of cls with params set from the parsed params dictionary
    """
    cls_specific_params = {}
    for k, v in cls.__dict__.items():
        if isinstance(v, BaseDescriptor):
            if params_to_omit is not None and k in params_to_omit:
                cls_specific_params[k] = None
                continue
            param_name = prefix + k if k not in parsed_params and prefix is not None else k
            if (params_to_hide is not None and param_name in params_to_hide) or \
                    param_name.startswith('_') or getattr(v, 'hide', False):
                continue
            if getattr(v, 'expand', False):
                unexpanded_param = _extract_expanded_param(parsed_params, param_name, v, prefix)
                cls_specific_params.update({k: unexpanded_param})
            else:
                if isinstance(parsed_params[param_name], Iterable) and \
                        not isinstance(parsed_params[param_name], str):
                    cls_specific_params[k] = [convert_to_si_units(p, getattr(v, 'unit', None))
                                              for p in parsed_params[param_name]]
                else:
                    cls_specific_params[k] = convert_to_si_units(parsed_params[param_name],
                                                                 getattr(v, 'unit', None))
        elif isinstance(v, Params):
            _params_to_omit = _get_omitted_params(v)
            next_prefix = _create_param_name_prefix(k, getattr(cls, '__nested_prefixes__', None))
            _prefix = prefix + next_prefix if prefix is not None else next_prefix
            cls_specific_params[k] = _unflatten_params_cls(type(v), parsed_params,
                                                           prefix=_prefix,
                                                           params_to_omit=_params_to_omit,
                                                           params_to_hide=_get_hidden_params(cls))
    return cls(**cls_specific_params)


def to_argparse(cls: type(Params), **kwargs) -> ArgumentParser:
    """
    Convert a Params class or subclass to an argparse argument parser.
    """
    parser = ArgumentParser(description=cls.__doc__, **kwargs)

    # first, we flatten the cls params (means flattening any nested Params classes)
    flattened_params = _flatten_cls_params(cls)

    # merge any positional arguments
    params_to_delete, positional_param = _merge_positional_params(list(flattened_params.items()))
    for p in params_to_delete:
        del flattened_params[p]
    if positional_param is not None:
        flattened_params['positionals'] = positional_param

    # actually add the params to the argument parser
    hidden_params = _get_hidden_params(cls)
    for name, param in flattened_params.items():
        # don't expose hidden params through argparse
        if getattr(param, 'hide', False) or name in hidden_params or name.startswith('_'):
            continue
        _add_param_to_parser(name, param, parser)

    assert sum(getattr(p, 'nargs', '') not in ['+', '*', '?'] for p in vars(cls).values()
               if getattr(p, 'positional', False)) <= 1, \
        'Behavior is undefined for multiple positional arguments with nargs=+|*|?'
    return parser


def from_parsed_args(*cls_list, params_namespace: Namespace) -> Tuple[Params]:
    """
    Convert a list of params classes and an argparse parsed namespace to a list of class instances
    """
    params = vars(params_namespace)
    flattened_classes = [_flatten_cls_params(cls) for cls in cls_list]
    # handle positional arguments
    positional_params = {}
    for flattened_cls in flattened_classes:
        positional_params.update({k: v for k, v in flattened_cls.items()
                                  if getattr(v, 'positional', False)})
    if 'positionals' in params:
        parsed_positionals = params['positionals']
        # now we must match the positional params to the list of positional arguments we got back
        matched_pos_args = _parse_positional_arguments(parsed_positionals,
                                                       positional_params)
        params.update(matched_pos_args)

    # actually construct the params classes
    return tuple(_unflatten_params_cls(cls, params) for cls in cls_list)


def create_parser_and_parse_args(*cls_list,
                                 throw_on_unknown: bool = False,
                                 **kwargs) -> Union[Tuple[Params], Params]:
    """
    Outside interface for creating a parser from multiple Params classes and parsing arguments
    """
    parser = to_argparse(merge_param_classes(*cls_list), **kwargs)
    args, argv = parser.parse_known_args()
    if argv != [] and throw_on_unknown:
        raise ValueError(f'Unknown arguments: {argv}')
    return from_parsed_args(*cls_list, params_namespace=args) \
        if len(cls_list) > 1 else from_parsed_args(*cls_list, params_namespace=args)[0]
