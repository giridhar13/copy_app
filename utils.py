def get_value_from_dict(data, key):
    """
    Recursively searches for a value in a nested dictionary or list.

    Args:
        data (dict or list): The dictionary or list to search in.
        key: The key to search for.

    Returns:
        The value associated with the key, if found. None otherwise.
    """
    if isinstance(data, dict):
        if key in data:
            return data[key]
        for k, v in data.items():
            result = get_value_from_dict(v, key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = get_value_from_dict(item, key)
            if result is not None:
                return result
    return None