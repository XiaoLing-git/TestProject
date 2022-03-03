from typing import List

from steps import __all__, Test6
from utils.steps import Step, StepType
from utils.suites import Suite, SuiteId, SuiteType


def create_provision_suite_steps() -> Suite:

    SuiteId.Suite1 = 'suite1'

    steps = []
    for i in __all__:
        s = i()
        steps.append(
            Step(stepId=str(s),
                 stepType=StepType.GENERIC,
                 _implementation=s))

    i = Test6(low_limit=50,high_limit=60)
    s = Step(stepId=str(i),
             stepType=StepType.GENERIC,
             _implementation=i,
             required=False)

    steps.append(s)

    suite1 = Suite(suiteid=SuiteId.Suite1,
                   suiteType = SuiteType.GENERIC,
                   steps = steps)
    return suite1


