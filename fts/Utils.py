
from functools import wraps

def database_invoke(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        # Get connection and cursor
        self.ConnectDatabase()
        # Execute function
        var = fn(self, *args, **kwargs)
        # Close the connection
        self.CloseDatabase()
        return var
    return wrapper
