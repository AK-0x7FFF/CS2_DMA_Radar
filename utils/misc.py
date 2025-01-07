from time import time, perf_counter
from typing import Self



class TimeCounter:
    def __enter__(self) -> None:
        self.t = perf_counter()

    def __exit__(self, _, __, ___) -> None:
        te = perf_counter()
        print("%.4fms" % ((te - self.t) * 1000))


class TimeoutCounter:
    _instance: dict[int, Self] = dict()

    def __new__(cls, counter_id: int):
        if (instance := cls._instance.get(counter_id, None)) is None:
            instance = super().__new__(cls)
            cls._instance.update({counter_id: instance})

        return instance

    def __init__(self, counter_id: int) -> None:
        self.id: int = counter_id
        self.target_time: float | None = None


    def start(self, timeout: float) -> Self:
        self.target_time = time() + timeout
        return self

    def check(self) -> bool:
        if self.target_time is None: return False

        time_now = time()
        if time_now > self.target_time: return True
        return False

    def time_left(self) -> float | None:
        if self.target_time is None: return None

        time_now = time()
        return self.target_time - time_now






def main() -> None:
    print(id(TimeoutCounter(1)))
    print(id(TimeoutCounter(1)))
    print(id(TimeoutCounter(2)))
    print(id(TimeoutCounter(2)))
    print(id(TimeoutCounter(1)))

if __name__ == '__main__':
    main()