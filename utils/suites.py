from pydantic import BaseModel,Field
from enum import Enum
from typing import List,Optional
from .steps import Step
from datetime import datetime


class SuiteType(str, Enum):
    """Suite types."""

    PROVISION_SYSTEM = "provision_system"
    Z_STAGE_TEST = "z_stage_test"
    MOTORS_TEST = "motors_test"
    BURN_IN_TEST = "burn_in_test"
    HARDWARE_TEST = "hardware_test"

    @classmethod
    def get_all_suites(cls) -> List:
        """Get an ordered list of all suite types."""
        return [
            cls.PROVISION_SYSTEM,
            cls.Z_STAGE_TEST,
            cls.MOTORS_TEST,
            cls.BURN_IN_TEST,
            cls.HARDWARE_TEST,
        ]


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

    suiteType: SuiteType = Field(..., description="The specific type of suite")
    steps: List[Step] = Field(..., description="Suite step list")
    status: SuiteStatus = Field(SuiteStatus.PENDING, description="Suite run status")
    startTime: Optional[datetime] = Field(
        None, description="When the suite was started"
    )
    endTime: Optional[datetime] = Field(
        None, description="When the suite finished, failed, or was cancelled"
    )
