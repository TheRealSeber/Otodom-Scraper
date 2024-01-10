def flatten_json(y: dict):
    """
    Flattens a JSON object to a single level.

    >>> flatten_json({"a": {"b": 1, "c": {"d": 2}})
        {"a_b": 1, "a_c_d": 2}
    """
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
