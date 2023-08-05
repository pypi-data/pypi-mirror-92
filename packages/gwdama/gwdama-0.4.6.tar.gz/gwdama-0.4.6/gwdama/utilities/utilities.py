"""
Utility functions
"""
# To define wrappers to enhance existing classes
from functools import wraps

def _add_property(cls):
    """
    Decorator to add properties to already existing classes.
    Partially based on the work of M. Garod:
    https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    
    Example
    -------
    To add theproperty `func` to the class Class:
    @_add_property(Class)
    def func(self):
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs): 
            return func(self,*args, **kwargs)
        setattr(cls, func.__name__, property(wrapper))
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator


def _add_method(cls):
    """
    Decorator to add methds to already existing classes.
    Partially based on the work of M. Garod:
    https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    
    Example
    -------
    To add theproperty `func` to the class Class:
    @_add_method(Class)
    def func(self):
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs): 
            return func(self,*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator

# def name_changer(obj, kay):
#     if not os.path.exists(outdir):
#         os.makedirs(outdir)
#     else:
#         expand = 0
#         while True:
#             expand += 1
#             new_event = event_id +'_'+ str(expand)
#             if os.path.exists(args.directory.rstrip('/')+'/'+new_event):
#                 continue
#             else:
#                 event_id = new_event
#                 break
#         outdir = args.directory.rstrip('/')+'/'+event_id
#         os.makedirs(outdir)	
