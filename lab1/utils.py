def convert_temp(val: tuple) -> float:
    if len(val) != 2:
        raise ValueError("wrong usage of convert_temp(): tuple must contain 2 values")
    if val[1] == 'K':
        return val[0] - 273.15
    if val[1] == 'F':
        return (val[0] - 32) * 5 / 9
    return val[0]
    

def g_float(a: float, b: float, diff: float = 1e-350):
    return a - b > diff
