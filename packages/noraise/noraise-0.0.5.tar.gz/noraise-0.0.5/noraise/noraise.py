# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Union, Any
import traceback
from functools import wraps

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def noraise(print_exc: bool = True, return_none_instead_of_error: bool = True) -> Union[Exception, Any]:
    """surpasses Exception raise

    Args:
        print_exc (bool, optional): Wether the stacktracee should be printed or not. Defaults to True.

    Returns:
        Union[Exception, Any]: if a raise is catched. The exception is returned as result
    """
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                if print_exc:
                    print('\n\n<-------------------------------- Caught with \'@noraise\' start -------------------------------->\n')
                    traceback.print_exc()
                    print('\n<--------------------------------- Caught with \'@noraise\' end --------------------------------->\n\n')

                return None if return_none_instead_of_error else e

        return wrapper
    return real_decorator


# ---------------------------------------------------------------------------------------------------------------------------------------- #
