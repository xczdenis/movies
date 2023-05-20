def normalize_value(value, target_type):
    if value is None:
        if target_type == int:
            return 0
        elif target_type == float:
            return 0.0
        elif target_type == str:
            return ""
    return value
