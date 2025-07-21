import pickle
import os
from typing import Any, Optional, Union

class DynCache:
    def __init__(self, use_memory: bool = True, temp_dir: Optional[str] = None):
        self._use_memory = use_memory
        
        if not (self._use_memory):
            if not (temp_dir):
                raise ValueError("temp_dir must be specified when not using memory mode")
            if not (os.path.isdir(temp_dir)):
                raise ValueError(f"Directory does not exist: {temp_dir}")
            
            self._temp_dir = os.path.normpath(temp_dir) + os.sep
        else:
            self._temp_dir = None
            
        self._memory_cache: dict[str, Any] = {}
        
    def _get_filepath(self, key: str) -> str:
        return os.path.join(self._temp_dir, f"{key}.cache")
    
    def get(self, key: str) -> Optional[Any]:
        if (self._use_memory):
            return self._memory_cache.get(key)
        
        filepath = self._get_filepath(key)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        return None
    
    def set(self, key: str, value: Any) -> None:
        if (self._use_memory):
            self._memory_cache[key] = value
        else:
            filepath = self._get_filepath(key)
            with open(filepath, 'wb') as f:
                pickle.dump(value, f)
    
    def clear(self, key: Optional[str] = None) -> None:
        if (self._use_memory):
            if key is not None:
                self._memory_cache.pop(key, None)
            else:
                self._memory_cache.clear()
        else:
            if (key is not None):
                filepath = self._get_filepath(key)
                if os.path.exists(filepath):
                    os.remove(filepath)
            else:
                for filename in os.listdir(self._temp_dir):
                    if filename.endswith('.cache'):
                        os.remove(os.path.join(self._temp_dir, filename))

    def increment(self, key: str, amount: Union[int, float] = 1) -> Union[int, float]:
        current = self.get(key) or 0
        if not (isinstance(current, (int, float))):
            raise TypeError(f"Cannot increment non-numeric value: {current}")
        
        new_value = current + amount
        self.set(key, new_value)
        return new_value

    def decrement(self, key: str, amount: Union[int, float] = 1) -> Union[int, float]:
        return self.increment(key, -amount)

    @property
    def mode(self) -> str:
        return "memory" if (self._use_memory) else f"disk: {self._temp_dir}"

    @property
    def temp_dir(self) -> Optional[str]:
        return self._temp_dir