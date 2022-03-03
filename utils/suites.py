import json

from pydantic import BaseModel, Field, Extra
from enum import Enum
from typing import List,Optional
from .steps import Step
from datetime import datetime


class SuiteId():
    __instance = None

    def  __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if SuiteId.__instance is None:
            SuiteId.__instance = object.__new__(cls)
        return SuiteId.__instance

    @classmethod
    def get_all_ids(cls):
        res = {}
        for k ,v in SuiteId.__dict__.items():
            if k.startswith("__") or k in "_SuiteId__instance get_all_ids" :
                continue
            res[k] = v
        return res


class SuiteType(str, Enum):
    """Suite types."""
    GENERIC = "generic"
    STRING_INPUT = "string_input"


class SuiteStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    AWAITING_INPUT = "awaiting_input"
    PASSED = "passed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ERROR = "error"

    def in_progress(self) -> bool:
        """Get if the status refers to a procedure that is executing."""
        return self in {
            SuiteStatus.RUNNING,
            SuiteStatus.AWAITING_INPUT,
        }


class Suite(BaseModel):
    """Station suite model."""
    suiteid :str = Field(..., description="Suite identifier")
    suiteType: SuiteType = Field(..., description="The specific type of suite")
    steps: List[Step] = Field(..., description="Suite step list")
    status: SuiteStatus = Field(SuiteStatus.PENDING, description="Suite run status")
    startTime: Optional[str] = Field(
        None, description="When the suite was started"
    )
    endTime: Optional[str] = Field(
        None, description="When the suite finished, failed, or was cancelled"
    )
    elapsed_time: Optional[str]=Field(None,description='elapsed_time')


    class Config:
        """Allow extra fields for the command implementation."""

        extra = Extra.allow

    def to_dict(self):
        response_dict = self.dict()
        # for i in self.dict():
        #     response_dict[i] = self.dict()[i]
        steps = []
        for i in self.steps:
            res=json.dumps(i.to_dict())
            res = json.loads(res)
            steps.append(res)
        response_dict['steps'] = steps
        return response_dict
