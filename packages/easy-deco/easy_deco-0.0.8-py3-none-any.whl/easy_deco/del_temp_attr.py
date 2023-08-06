import inspect


class Del_Temp_Attr(object):

    def __init__(self, cls):
        """

        """
        self._cls = cls
        
    def __call__(self, fn):
        """
        Decorator to delete all temporary attributes generated in each pipeline component

        **Parameters**

        * **:param fn:** (Function) function to be decorated
        """
        def wrapper(*args, **kwargs):

            result = fn(*args, **kwargs)
            cls = self._cls

            for instance in getattr(cls, "_instances"):

                for attr in list(instance.__dict__.keys()):

                    if attr.startswith('_') and attr.endswith('_'):

                        if not(attr.startswith('__') and attr.endswith('__')):
                            
                            delattr(instance, attr)

            return result

        return wrapper


class DelTempAttr(type):

    def __new__(meta, name, bases, class_dict):

        klass = super().__new__(meta, name, bases, class_dict)

        for key in dir(klass):
            
            value = getattr(klass, key)

            if not key.startswith('_'):

                del_attr = Del_Temp_Attr(klass)
                wrapped = del_attr(value)
                setattr(klass, key, wrapped)

        return klass