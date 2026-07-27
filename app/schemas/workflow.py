from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator

EventStatus = Literal["success", "failed", "warning", "pending"]

class WorkflowEvent(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    timestamp: datetime
    type: str = Field(min_length=1, max_length=100)
    status: EventStatus
    actor: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=500)
    metadata: dict[str, Any] = Field(default_factory=dict)

class WorkflowCreate(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    events: list[WorkflowEvent] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_event_ids(self):
        ids = [event.id for event in self.events]
        if len(ids) != len(set(ids)):
            raise ValueError("Event IDs must be unique within a workflow")
        return self

class WorkflowResponse(WorkflowCreate):
    pass

class WorkflowSummary(BaseModel):
    id: str
    name: str
    event_count: int

class WorkflowAnalytics(BaseModel):
    workflow_id: str
    total_events: int
    successful_events: int
    failed_events: int
    warning_events: int
    duration_seconds: float
    longest_gap_seconds: float
    success_rate: float

class WorkflowComparisonRequest(BaseModel):
    baseline_workflow_id: str
    candidate_workflow_id: str

class WorkflowComparison(BaseModel):
    baseline_workflow_id: str
    candidate_workflow_id: str
    duration_difference_seconds: float
    event_count_difference: int
    failed_event_difference: int
    missing_event_types: list[str]
    additional_event_types: list[str]
