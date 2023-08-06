from abc import ABCMeta, abstractmethod
from typing import List, Optional, TypeVar, Generic

from dynamo_dao.dynamo import DynamoClient, DynamoObject, DynamoValue


T = TypeVar("T")


class Dao(Generic[T], metaclass=ABCMeta):
    def __init__(self) -> None:
        self._dynamo = DynamoClient()

    @property
    @abstractmethod
    def table_name(self) -> str:
        pass

    @property
    @abstractmethod
    def unique_key(self) -> List[str]:
        pass

    @abstractmethod
    def convert_to_dynamo(self, var: T) -> DynamoObject:
        pass

    @abstractmethod
    def convert_from_dynamo(self, var: DynamoObject) -> T:
        pass

    def create(self, item: T) -> None:
        dynamo_object = self.convert_to_dynamo(item)

        self._dynamo.create(self.table_name, dynamo_object)

    def read(self, key: Optional[str], value: Optional[DynamoValue]) -> List[T]:
        raw = self._dynamo.read(self.table_name, key, value)

        if not raw:
            return []

        return [self.convert_from_dynamo(r) for r in raw]

    def read_one(self, key: str, value: DynamoValue) -> Optional[T]:
        result = self.read(key, value)

        if len(result) == 0:
            return None

        return result[0]

    def read_one_or_die(self, key: str, value: DynamoValue) -> T:
        result = self.read_one(key, value)

        if not result:
            raise Exception("not found")

        return result

    def update(self, original: T, updated: T) -> None:
        original_dyanmo = self.convert_to_dynamo(original)
        updated_dynamo = self.convert_to_dynamo(updated)

        unique_key = {
            unique_key_column: original_dyanmo[unique_key_column]
            for unique_key_column in self.unique_key
        }

        unique_key = {}
        for unique_key_column in self.unique_key:
            if original_dyanmo[unique_key_column] != updated_dynamo[unique_key_column]:
                raise Exception("updated entity must have the same key as the original")

            unique_key[unique_key_column] = original_dyanmo[unique_key_column]

        updated_attributes: List[str] = []
        for key, value in updated_dynamo.items():
            if value != original_dyanmo[key]:
                self._dynamo.update(self.table_name, unique_key, key, value)
                updated_attributes.append(key)

        return
