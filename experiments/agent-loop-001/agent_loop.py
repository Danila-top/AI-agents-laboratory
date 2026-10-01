"""Minimal observable agent loop baseline.

The implementation intentionally keeps planning and verification explicit so the
experiment can measure each stage independently.
"""

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class RunResult(Generic[T]):
    attempts: int
    value: T
    verified: bool


class AgentLoop(Generic[T]):
    def __init__(
        self,
        observe: Callable[[], object],
        plan: Callable[[object], T],
        act: Callable[[T], T],
        verify: Callable[[T], bool],
        max_attempts: int = 3,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        self.observe = observe
        self.plan = plan
        self.act = act
        self.verify = verify
        self.max_attempts = max_attempts

    def run(self) -> RunResult[T]:
        last = None
        for attempt in range(1, self.max_attempts + 1):
            observation = self.observe()
            plan = self.plan(observation)
            last = self.act(plan)
            if self.verify(last):
                return RunResult(attempt, last, True)
        return RunResult(self.max_attempts, last, False)


if __name__ == "__main__":
    loop = AgentLoop(
        observe=lambda: "calculate 2 + 2",
        plan=lambda observation: observation,
        act=lambda task: 4 if task == "calculate 2 + 2" else None,
        verify=lambda result: result == 4,
    )
    result = loop.run()
    print(result)
