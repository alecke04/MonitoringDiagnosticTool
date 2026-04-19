from abc import abstractmethod, ABC


class DbClass(ABC):
    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    @abstractmethod
    def get_table_structure(cls):
        pass

    @classmethod
    def get_table_creation_string(cls):
        columns = cls.get_table_structure()
        column_defs = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
        return f"CREATE TABLE IF NOT EXISTS {cls.get_name()} ({column_defs});"

