import time

from utils.steps import StepImplementation, StepId, Step


class Test1(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test1 = "math"

    def execute(self) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(100):
            time.sleep(0.05)
            sum = sum + i
            # print(sum)

        return sum


class Test2(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test2 = "math2"

    def execute(self,**kwargs) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(20):
            time.sleep(0.05)
            sum = sum + i
            # print(sum)

        return sum

    def should_repeat(self, *args):
        return 6


class Test3(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test3 = "math3"

    def execute(self, ) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(150):
            time.sleep(0.2)
            sum = sum + i
            # print(sum)

        return sum
