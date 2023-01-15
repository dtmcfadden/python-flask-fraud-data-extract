

def convert_tuple_to_dict(t):
    if t:
        return dict((y, x) for x, y in t)
    else:
        return {}
