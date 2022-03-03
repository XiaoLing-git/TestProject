import json

from runner.suiteRunner import SuiteRunner
from suites.suitedemo import create_provision_suite_steps
from utils.suites import SuiteId

suite = create_provision_suite_steps()
# print(suite.to_dict())
# print(SuiteId.get_all_ids())

s = SuiteRunner(suite)
res = s.run()
# print(res)
# res= json.dumps(res)
# print(res)
# res = json.loads(res)
# print(res)
# s.output_file()




