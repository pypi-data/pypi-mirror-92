"""Math functions, no variables"""

import typing as tp
import decimal as dc

_meganum = tp.Union[int, float, dc.Decimal, tp.SupportsInt, tp.SupportsFloat]
_num = tp.Union[int, float, dc.Decimal]
_micronum = tp.Union[int, float]
_decnum = tp.Union[float, dc.Decimal]

def _total_round(value: _num, precision: int = 10, decimal: bool = False) -> _num:
    """Rounds 'value' to the nearest 'precision' digits."""
    if isinstance(value, int):
        return value
    elif precision < 0:
        raise ValueError('Cannot cast a negative integer onto \'xm._total_round(precision)\'')
    elif decimal is True:
        if isinstance(value, dc.Decimal):
            return round(value, precision)
        elif not isinstance(value, dc.Decimal) and decimal is True:
            raise TypeError('Cannot cannot cast \'float\' onto \'xm._total_round(value)\' \
with opperand \'decimal\' as \'True\'.')
    elif decimal is False:
        if isinstance(value, float):
            return round(value, precision)
        elif not isinstance(value, float):
            raise TypeError('Cannot cast \'decimal\' onto \'xm._total_round(value)\' \
with opperand \'decimal\' as \'False\'.')
    
def summation(count: int, bottom_var: str, expression: str, precision: int = 10, \
decimal: bool = False) -> _num:
    '''Summation function. Example: 'summation(4, 'z=1', 'z+1')' would return 14.'''
    
    if precision < 0:
        raise ValueError('Cannot cast a negative integer onto \'xm.summation(precision)\'')
    var, value = bottom_var.split('=')
    var = var.strip()
    
    if decimal is True:
        value = dc.Decimal(eval(value))
    else:
        value = int(eval(value))

    res = 0
    for i in range(value, count+1):
        res += eval(expression.replace(var, str(i)))

    if decimal is True:
        return _total_round(value=res, precision=precision, decimal=True)
    return _total_round(res, precision=precision, decimal=False)

def sq(value: _num, precision: int = 10, decimal: bool = False, _print_unround: bool = False) -> _micronum:
    '''Returns 'value' raised to the 2nd power, with 'precision' decimal points.'''
    if isinstance(value, float) and decimal is True:
        raise TypeError('Cannot cannot cast \'float\' onto \'xm.cb\' \
with opperand \'decimal\' as \'True\'.')
    elif isinstance(value, dc.Decimal) and decimal is False:
        raise TypeError('Cannot cannot cast \'decimal\' onto \'xm.cb\' \
with opperand \'decimal\' as \'False\'.')
    elif isinstance(value, dc.Decimal) and decimal is True:
        if _print_unround is True:
            print(value*value)
        return _total_round(value*value, precision, decimal=True)
    if _print_unround is True:
        print(value*value)
    return _total_round(value*value, precision, decimal=False)

def sqrt(value: _meganum, precision: int = 10, decimal: bool = False, _print_unround: bool = False):
    if decimal is True:
        x = dc.Decimal(value)
        y = dc.Decimal(1)
        e = dc.Decimal(0.000000000000000000000000000000000000000000000000000000000000000001)
    else:
        x = value
        y = 1
        e = 0.0000000000000000000000001
    
    while x - y > e:
        x = (x + y)/2
        y = value / x

    if _print_unround is True:
        print(x)

    return(_total_round(x, precision, decimal=decimal))

def cb(value: _meganum, precision: int = 10, decimal: bool = False, _print_unround: bool = False) -> _num:
    '''Returns 'value' raised to the 2nd power, with '''
    if isinstance(value, float) and decimal is True:
        raise TypeError('Cannot cannot cast \'float\' onto \'xm.cb\' \
with opperand \'decimal\' as \'True\'.')
    elif isinstance(value, dc.Decimal) and decimal is False:
        raise TypeError('Cannot cannot cast \'decimal\' onto \'xm.cb\' \
with opperand \'decimal\' as \'False\'.')
    elif isinstance(value, dc.Decimal) and decimal is True:
        if _print_unround is True:
            print(value*value*value)
        return _total_round(value*value*value, precision, decimal=True)
    if _print_unround is True:
        print(value*value*value)
    return _total_round(value*value*value, precision, decimal=False)

def cbrt(value, _print_unround: bool = False) -> _num:
    x = value**(1/3)

    if _print_unround is True:
        print(x)

    if type(x) is float:
        if round(x, 10) == int(round(x, 10)): return int(round(x, 10))
        return round(x, 10)
    return x

# def xpn(base: _meganum, exponent: _meganum, decimal: bool = False, _print_debug: bool = False) \
# -> _num:
#     out = 1
#     if exponent == 0:
#         print('\'exponent\' is 0, x^0=1.')
#         return 1
#     elif int(exponent/3) == exponent/3:
#         if _print_debug is True:
#             print('\'exponent\' is a multiple of 3.')
#         repeat = int(exponent/3)
#         for i in range(repeat):
#             out *= cb(base)
#             if _print_debug is True:
#                 print(out)
#         return out
#     elif int(exponent/2) == exponent/2:
#         if _print_debug is True:
#             print('\'exponent\' is a multople of 2.')
#     else:
#         print('\'exponent\' is not multiple of 2 or 3.')
