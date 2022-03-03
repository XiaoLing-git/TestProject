import datetime
import json
import os
import time

from runner.stepRunner import StepRunner
from utils.steps import StepId, Step, StepType, StepStatus
from utils.suites import SuiteId, Suite
from pathlib import Path


class SuiteRunner():
    def __init__(self,
                 suite: Suite,
                 path: Path = None):
        self.suite = suite
        self._path = path
        self.T = datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S")

        self.init_time = None
        self.end_time = None
        self.elapsed_time = None

        self.suite_id = self.suite.suiteid
        self.steps_list = self.suite.steps
        self._create_folder()

    def append_step(self,
                    step: Step):
        return self.steps_list.append(step)

    def _before_run(self):
        self.init_time = datetime.datetime.now()
        self.suite.startTime = self.init_time.strftime("%Y/%m/%d/ %H:%M:%S")

    def _run(self, **kwargs):
        try:
            for i in self.steps_list:
                steprunner = StepRunner(i, path=self._path)
                steprunner.run()
        except Exception:
            pass
        finally:
            pass

        return self.suite.to_dict()

    def _after_run(self):
        # from datetime import timedelta
        self.end_time = datetime.datetime.now()
        self.elapsed_time= self.end_time - self.init_time

        self.suite.endTime = self.end_time.strftime("%Y/%m/%d/ %H:%M:%S")
        self.suite.elapsed_time = self.elapsed_time.total_seconds()

    def _on_step_error(self, error: Exception):
        pass

    def run(self, **kwargs):
        self._before_run()
        res = self._run()
        self._after_run()
        self.output_file()
        return res

    def output_file(self):
        output_file_name = os.path.join(self._path, self.suite_id + self.T +  '.json')
        with open(output_file_name, 'w') as file:
            json.dump(
                self.suite.to_dict(),
                file,
                sort_keys=False,
                indent=4,
                separators=(',', ': ')
            )

    def _create_folder(self):
        if self._path is None:
            base_dir = os.path.dirname(os.path.abspath(__name__))
            self._path = Path(os.path.join(os.path.join(base_dir, 'results'),
                                           str(self.suite_id) + self.T))
            # print(self._path)
            if not self._path.exists():
                os.makedirs(self._path)
        else:
            if not self._path.exists():
                raise IOError("Path is not exist")
            else:
                self._path = self._path.joinpath(Path("{}\\{}{}".
                                                      format("results", self.suite_id, self.T)))
                os.makedirs(self._path)
