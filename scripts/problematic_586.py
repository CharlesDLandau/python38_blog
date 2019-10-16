def problematic_586(k: int):
    if k < 100:
        return k
    else:
        raise ValueError('Gotta be less than 100')
problematic_586(144)