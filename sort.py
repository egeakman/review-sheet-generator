class Sort:
    @staticmethod
    def sort_nested(data, sort_keys: list[str]):
        def get_sort_key(item):
            return tuple(item.get(key, "") for key in sort_keys)

        if isinstance(data, dict):
            return {
                key: (
                    Sort.sort_nested(value, sort_keys)
                    if isinstance(value, (dict, list))
                    else value
                )
                for key, value in data.items()
            }
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                return sorted(
                    (Sort.sort_nested(item, sort_keys) for item in data),
                    key=get_sort_key,
                )
            else:
                return sorted(
                    (
                        Sort.sort_nested(item, sort_keys)
                        if isinstance(item, (dict, list))
                        else item
                    )
                    for item in data
                )
        else:
            return data
