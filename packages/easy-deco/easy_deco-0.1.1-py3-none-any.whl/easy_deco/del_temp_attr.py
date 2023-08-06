import inspect

def del_temp_attr(fn):
    """
    Decorator to delete all temporary attributes generated in each pipeline component

    **Parameters**

    * **:param fn:** (Function) function to be decorated
    """
    def wrapper(*args, **kwargs):

        result = fn(*args, **kwargs)
        cls = args[0]

        for instance in getattr(cls, "_instances"):
            
            for attr in list(instance.__dict__.keys()):

                if attr.startswith('_') and attr.endswith('_'):

                    if not(attr.startswith('__') and attr.endswith('__')):

                        delattr(instance, attr)

        return result

    return wrapper


def set_to_methods(decorator):

    def decorate(cls):

        attrs = inspect.getmembers(cls, predicate=lambda x: inspect.isroutine(x))

        for attr, _ in attrs:
            
            if not attr.startswith('_'):

                setattr(cls, attr, decorator(getattr(cls, attr)))
        
        return cls

    return decorate