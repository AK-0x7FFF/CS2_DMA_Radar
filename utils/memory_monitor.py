from typing import Callable, Any


class MemoryMonitor:
    enable: bool = True
    memory_read_count: int = 0
    memory_read_bytes: int = 0

    @classmethod
    def read_count_add(cls, count: int = 1) -> None:
        cls.memory_read_count += count

    @classmethod
    def read_bytes_add(cls, size: int) -> None:
        cls.memory_read_bytes += size

    @classmethod
    def reset_read(cls) -> None:
        cls.memory_read_count = 0
        cls.memory_read_bytes = 0

    @classmethod
    def reset(cls) -> None:
        cls.reset_read()


    @staticmethod
    def read_decorator(byte_size_call: Callable[[tuple, dict], int]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable) -> Callable:
            def wrapper(*func_args, **func_kwargs) -> Any:
                if MemoryMonitor.enable:
                    MemoryMonitor.read_count_add()
                    MemoryMonitor.read_bytes_add(byte_size_call(func_args, func_kwargs))

                try: return func(*func_args, **func_kwargs)
                except Exception: return None
            return wrapper
        return decorator