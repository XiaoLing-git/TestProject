import random
import time

from utils.steps import StepImplementation, StepId, Pass_Flag, Fail_Flag


class Test1(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test1 = "math"

    def execute(self) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(100):
            time.sleep(0.05)
            sum = sum + i
            if sum > 300:
                raise Pass_Flag(sum)
            # print(sum)

        return sum


class Test2(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test2 = "math2"

    def execute(self) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(20):
            time.sleep(0.05)
            sum = sum + i
            # print(sum)

        return sum

    def should_repeat(self):
        return 6


class Test3(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test3 = "math3"

    def execute(self) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(150):
            time.sleep(0.1)
            sum = sum + i
            # print(sum)

        return sum


class Test4(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test4 = "math4"

    def execute(self) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(100):
            time.sleep(0.05)
            sum = sum + i
            # print(sum)

        return sum


class Test5(StepImplementation):
    """A step to check system time against operator time."""

    StepId.Test5 = "math5"

    def execute(self) -> str:
        """Confirm time execution implementation."""
        sum = 0
        for i in range(20):
            time.sleep(0.05)
            sum = sum + i
            # print(sum)

        return sum

    def should_repeat(self):
        return 6


class Test6(StepImplementation):
    """A step to check system time against operator time."""
    StepId.Test6 = "math6"

    def __init__(self,high_limit,low_limit):
        self.high_limit=high_limit
        self.low_limit=low_limit

    def execute(self,) -> str:
        """Confirm time execution implementation."""
        sum = random.randint(0,100)
        if sum> self.low_limit and sum< self.high_limit:
            raise Pass_Flag(sum)
        else:
            return str(sum)

    def should_repeat(self, *args):
        return 100
