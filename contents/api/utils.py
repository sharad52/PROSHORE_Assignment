def str_to_bool(val):
    if val in ['True', 'true']:
        return True
    elif val in ['False', 'false']:
        return False
    return val