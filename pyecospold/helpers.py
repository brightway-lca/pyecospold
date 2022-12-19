class DataTypesConverter:
    @staticmethod
    def str_to_bool(string: str) -> bool:
        return string.lower() == "true"
