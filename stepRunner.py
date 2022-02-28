import time

from utils.steps import Step, StepStatus


class StepRunner:
    def __init__(self,step:Step):
        self.step = step
        self.init_time = None
        self.end_time = None
        self.elapsed_time = None
        self.cycle = 1
        self.count = 1
        self.result = {}

    def _before_run(self):
        # 1 set status as pending
        self.step.status = StepStatus.PENDING
        # 2 init start time
        self.init_time = time.time()
        # 3 get cycles
        if self.step.get_impl().should_repeat():
            self.cycle = self.step.get_impl().should_repeat()

    def _run(self,**kwargs):
        # 1 get init stage time
        stage_time = time.time()
        # 2 run execute
        res = self.step.get_impl().execute(**kwargs)
        # 3 print status information
        self.result["cycle"+str(self.count)] = {"Response":res,
                                        "Time":round(time.time() - stage_time,2)}

    def _after_run(self):
        # 1 get end time
        self.end_time = time.time()
        # 2 get elapsed time
        self.elapsed_time = round(self.end_time - self.init_time,2)
        # 3 get output data
        self.step.outputData = [self.result]
        # 4 update status
        self.step.status = StepStatus.DONE

    def _on_step_error(self,error:Exception):
        self.step.status = StepStatus.ERROR

    def run(self,**kwargs):
        try:
            # 1 init before run this step
            self._before_run()
            # 2 update status
            self.step.status = StepStatus.RUNNING
            # 3 run execute
            while self.count <= self.cycle:
                self._run(**kwargs)
                self.count  = self.count + 1
            # 4 update status
            self._after_run()
        except KeyboardInterrupt as e:
            # if canceled by hand , update status
            self.step.status = StepStatus.CANCELLED
            self.result['error'] = "Canceled"
        except Exception as e:
            # if get error while test , update status
            self.step.status = StepStatus.ERROR
            self.result['error'] = str(e)
        finally:
            self.step.outputData = self.result