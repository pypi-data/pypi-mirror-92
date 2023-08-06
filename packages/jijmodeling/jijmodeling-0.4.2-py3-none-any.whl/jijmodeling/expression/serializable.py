import inspect
import jijmodeling
from typing import Union




def to_serializable(term)->dict:
    """Convert to serializable object (dict)

    Assign the argument of constructor __init__ to the key named attribute.
    So each Expression class must have a property with the same name or underscore prefix as the constructor argument.
    When deserializing, the constructor of each Expression class is called 
    with the object stored in this attribute to construct the same mathematical model tree (Expression object).

    Args:
        term (jijmodeling.expression.Expression): source object.

    Returns:
        dict: serializable dict object.

    Example:
        >>> import jijmodeling as jm
        >>> n = jm.Placeholder("n")
        >>> x = jm.BinaryArray("x", n)
        >>> s_obj = jm.to_serializable(x)
        >>> import pprint
        >>> pprint.pprint(s_obj)
        {'attributes': {'shape': {'iteratable': 'tuple',
                                  'value': [{'attributes': {'label': 'n'},
                                             'class': 'jijmodeling.variables.variable.Placeholder',
                                             'version': '0.3.*'}]},
                        'variable': {'attributes': {'children': {'iteratable': 'tuple',
                                                                'value': []},
                                                    'label': 'x'},
                                     'class': 'jijmodeling.variables.variable.Binary',
                                     'version': '0.3.*'}},
        'class': 'jijmodeling.variables.array.Array',
        'version': '0.3.*'}
    """
    from jijmodeling.expression.expression import Children
    serializable = {
        'version': '0.3.0',
        'class': term.__class__.__module__ + '.' + term.__class__.__name__
    }
    def express_to_serializable(s):
        if 'to_serializable' in dir(s):
            return s.to_serializable()
        elif isinstance(s, (list, tuple, Children)):
            return {
                'iteratable': 'list' if isinstance(s, list) else 'tuple',
                'value': [express_to_serializable(t) for t in s]
            }
        elif isinstance(s, dict):
            return {k: express_to_serializable(v) for k,v in s.items()}
        else:
            return s

    init_args_keys =inspect.getfullargspec(term.__class__.__init__).args
    attributes = list(vars(term).keys())
    init_params = {}
    for k in init_args_keys:
        if k == 'self':
            continue
        attr_value = '_' + k if '_' + k in attributes else k
        init_params[k] = express_to_serializable(eval('term.{}'.format(attr_value)))

    serializable['attributes'] = init_params

    return serializable




def _cls_serializable_validation(serializable: dict, cls):
    if 'class' not in serializable:
        return None
    class_name = serializable['class'].split('.')[-1]
    if cls.__name__ != class_name:
        raise ValueError('Class "{}" is not class "{}"'.format(cls.__name__, class_name))
    


def from_serializable(serializable: Union[dict, list])->Union[dict, tuple, list]:
    """Generate initilize parameters of Expression from serializable object (dict object)

    Args:
        serializable (Union[dict, list]): [description]

    Returns:
        Union[dict, tuple, list]: [description]

    ver 0.3.*

    .. code-block:: json
    
        {  
            "version": "0.3.*",  
            "class": "Class name (ex. Array, Placeholder, Add, Prod, ...)",  
            "attributes": dict, # see below.  
        }  

        "attributes": Specifies the correspondence between the children's index and the name of each object. 
                      By default, this correspondence is an argument to __init__. 
                      The Sum class is not limited to this because the arguments of __init__ of it has a special shape.
    """
    if isinstance(serializable, dict) and 'class' in serializable:
        # Get module object from module string (ex: jijmodeling.array.Array)
        modulePath = serializable['class'].split('.')[1:]
        module = jijmodeling
        for m in modulePath:
            module = getattr(module, m)
        _cls_serializable_validation(serializable, module)
        return module.from_serializable(serializable)

    # If object is iteratable (ex. list or tuple) dict object has key (iteratable)
    elif isinstance(serializable, dict) and 'iteratable' in serializable:
        if serializable['iteratable'] == 'list':
            return [from_serializable(s) for s in serializable['value']]
        elif serializable['iteratable'] == 'tuple':
            return tuple(from_serializable(s) for s in serializable['value'])
    
    elif isinstance(serializable, list):
        return [from_serializable(s) for s in serializable]
    elif isinstance(serializable, dict):
        return {k: from_serializable(v) for k, v in serializable.items()}

    return serializable