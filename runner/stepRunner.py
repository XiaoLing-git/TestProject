import datetime
import time, json
import os

from pathlib import Path
from utils.steps import Step, StepStatus, Pass_Flag, Fail_Flag


class StepRunner:
    def __init__(self, step: Step, path: Path = None):
        self.step = step
        self.init_time = None
        self.end_time = None
        self.elapsed_time = None
        self.cycle = 1
        self.count = 1
        self.result = {}
        self.output = None
        self._path = path
        self.T = datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S")
        self.output_file_name = None
        self.response = None
        self.stagetime = None

    def _create_folder(self):
        if self._path == None:
            base_dir = os.path.dirname(os.path.abspath(__name__))
            self._path = Path(os.path.join(base_dir,'results'))
            if not self._path.exists():
                self._path.mkdir()
        else:
            if not self._path.exists():
                raise IOError("Path is not exist")

    def _before_run(self):
        self._create_folder()
        # 1 set status as pending
        self.step.status = StepStatus.PENDING
        # 2 init start time
        self.init_time = time.time()
        # 3 get cycles
        if self.step.get_impl().should_repeat():
            self.cycle = self.step.get_impl().should_repeat()

    def _run(self, **kwargs):
        # 1 get init stage time
        self.stagetime = time.time()
        # 2 run execute
        self.response = self.step.get_impl().execute(**kwargs)
        # 3 print status information
        self.result["cycle" + str(self.count)] = {"Response": self.response,
                                                  "Time": round(time.time() - self.stagetime, 2)}

    def _after_run(self):
        # 1 get end time
        self.end_time = time.time()
        # 2 get elapsed time
        self.elapsed_time = round(self.end_time - self.init_time, 2)
        # 3 get output data
        self.step.outputData = [self.result]
        # 4 update status
        self.step.status = StepStatus.DONE

    def _on_step_error(self):
        self.step.status = StepStatus.ERROR

    def run(self, **kwargs):
        try:
            # 1 init before run this step
            self._before_run()
            # 2 update status
            self.step.status = StepStatus.RUNNING
            # 3 run execute
            while self.count <= self.cycle:
                self._run(**kwargs)
                self.count = self.count + 1
            # 4 update status
            self._after_run()
        except KeyboardInterrupt as e:
            # if canceled by hand , update status
            self.step.status = StepStatus.CANCELLED
            self.result['error'] = "Canceled"
        except Pass_Flag as e:
            self.step.status = StepStatus.PASS
            self.result["cycle" + str(self.count)] = \
                {"Response": e.response,"Time": round(time.time() - self.stagetime, 2)}
        except Fail_Flag as e:
            self.step.status = StepStatus.FAIL
            self.result["cycle" + str(self.count)] = \
                {"Response": e.response,"Time": round(time.time() - self.stagetime, 2)}
        except Exception as e:
            # if get error while test , update status
            self._on_step_error()
            self.result['error'] = str(e)
        finally:
            self.elapsed_time = round(time.time() - self.init_time, 2)
            self.step.elapsed_time = self.elapsed_time
            self.step.outputData = self.result
            self.output = self.step.to_dict()
            self.output_file_name = os.path.join(self._path,self.step.stepId+ self.T + '.json')

            with open(self.output_file_name, 'w') as file:
                json.dump(
                    self.output,
                    file,
                    sort_keys=False,
                    indent=4,
                    separators=(',', ': ')
                )
