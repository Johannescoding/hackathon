"""file for wrappers. Only purpose is to make the code look not so messy"""
from functools import wraps

# only for functions that have ALWAYS the same output value
def download_wrapper(function):
    """Provides wrapping logic for all function that have ALWAYS! the same output values
        Content doesnt have to be downloaded twice for example"""
    @wraps(function)
    def wrapped(*args, **kwargs):
        if function.was_called:
            return function.return_value
        function.return_value = function(*args, **kwargs)
        function.was_called = True
        return function.return_value
    
    function.was_called = False
    return wrapped
