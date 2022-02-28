from enum import Enum
from pydantic import Field,BaseModel,Extra
from typing import Optional, Tuple, List
from abc import ABC,abstractmethod


class StepId():
    __instance = None

    def  __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if StepId.__instance is None:
            StepId.__instance = object.__new__(cls)
        return StepId.__instance

    @classmethod
    def get_all_ids(cls):
        res = {}
        for k ,v in StepId.__dict__.items():
            if k.startswith("__") or k in "_StepId__instance get_all_ids" :
                continue
            res[k] = v
        return res


class StepType(str, Enum):
    GENERIC = "generic"
    STRING_INPUT = "string_input"
    TIME_INPUT = "time_input"
    YES_NO_INPUT = "yes_no_input"
    PROCEED_INPUT = "proceed_input"
    IMAGE_OUTPUT = "image_output"


class StepStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    AWAITING_INPUT = "awaiting_input"
    DONE = "done"
    CANCELLED = "cancelled"
    ERROR = "error"

    def in_progress(self) -> bool:
        """Get if the status refers to a procedure that is executing."""
        return self in {
            StepStatus.RUNNING,
            StepStatus.AWAITING_INPUT,
        }


class StepImplementation(ABC):
    """Suite step execution implementation."""

    @abstractmethod
    def execute(
        self, **kwargs
    ) -> str:
        """Execute the command, producing a string output."""
        ...

    def should_repeat(self, *args) -> bool:
        """Determine whether the step should repeat."""
        return False


class Step(BaseModel):
    stepId: str = Field(..., description="Step identifier")
    stepType: StepType = Field(..., description="Step behavior type")
    status: StepStatus = Field(default=StepStatus.PENDING, description="Step status")
    inputData: Optional[str] = Field(default=None, description="Input data, if any")
    outputData: Tuple[str, ...] = Field(default=(), description="Output data, if any")
    required: bool = Field(default=True, description="Step required for suite to pass")
    fatal: bool = Field(default=False, description="Suite should end if step fails")
    _implementation: StepImplementation

    def get_impl(self,**kwargs) -> StepImplementation:
        """Get the step execution implementation."""
        return self._implementation

    class Config:
        """Allow extra fields for the command implementation."""

        extra = Extra.allow

    def to_dict(self):
        response_dict = {}
        for i in self.dict():
            if not i.startswith('_'):
                response_dict[i]  =self.dict()[i]
        return response_dict