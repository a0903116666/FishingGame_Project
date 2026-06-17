def clamp(value, lower, upper):
    return min(max(value, lower), upper)

def lerp(a, b, t):
    t = clamp(t, 0, 1)
    return a * (1 - t) + b * t