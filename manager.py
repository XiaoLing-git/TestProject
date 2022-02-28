from stepRunner import StepRunner
from utils.steps import StepId, Step, StepType, StepStatus
from steps.math import Test1
from steps.math import Test2
import json


s1 = Step(stepId=StepId.get_all_ids()['Test1'],
          stepType = StepType.GENERIC,
          _implementation =Test1() )

s2 = Step(stepId=StepId.get_all_ids()['Test2'],
          stepType = StepType.GENERIC,
          _implementation =Test2() )


for i in [s1,s2]:
    s = StepRunner(i)
    s.run()
    with open(i.stepId + '.json', 'w') as file:
        json.dump(
            i.to_dict(), file, sort_keys=False, indent=4, separators=(',', ': ')
        )
