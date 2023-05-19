def normalize_value(value, type):
    if value is None:
        if type == int:
            return 0
        elif type == float:
            return 0.0
        elif type == str:
            return ""
    return value
