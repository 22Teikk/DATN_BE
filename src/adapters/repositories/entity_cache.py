from abc import ABC, abstractmethod


class EntityCache(ABC):

    @abstractmethod
    def set_cache(
        self,
        key: str,
        values: list[dict],
        expire:int=0 ,
        cache_db: int = 0,
        chunk_size: int = 10000,
    ):
        """
        Set the value of a key in the cache.
        Args:
            key (str): The key to set.
            value (str): The value to set.
            expire (int): The expiration time in seconds.
        """
        pass

    @abstractmethod
    def get_cache(self, key: str) -> list[dict]:
        """
        Get the value of a key in the cache.

        Args:
            key (str): The key to get.
        """
        pass

    @abstractmethod
    def find_cache_keys(self, key_pattern: str) -> list[str]:
        """
        Find all keys that match the pattern.
        """
        pass

    @abstractmethod
    def delete_cache(self, key_pattern: str):
        """
        Delete the value of a key in the cache.
        """
        pass

    @abstractmethod
    def clean_cache(self):
        """
        Clean all keys in the cache.
        """
        pass

    @abstractmethod
    def get_cache_manager(self):
        pass
