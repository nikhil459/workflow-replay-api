from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.workflow import WorkflowRecord
from app.schemas.workflow import WorkflowAnalytics, WorkflowComparison, WorkflowComparisonRequest, WorkflowCreate, WorkflowEvent, WorkflowResponse, WorkflowSummary
from app.services.analytics import calculate_analytics
from app.services.comparison import compare_workflows

router = APIRouter()

def to_schema(record: WorkflowRecord) -> WorkflowCreate:
    return WorkflowCreate(id=record.id, name=record.name, events=[WorkflowEvent.model_validate(e) for e in record.events])

def get_record_or_404(workflow_id: str, db: Session) -> WorkflowRecord:
    record = db.get(WorkflowRecord, workflow_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return record

@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(payload: WorkflowCreate, db: Session = Depends(get_db)):
    if db.get(WorkflowRecord, payload.id):
        raise HTTPException(status_code=409, detail="A workflow with this ID already exists")
    db.add(WorkflowRecord(id=payload.id, name=payload.name, events=[e.model_dump(mode="json") for e in payload.events]))
    db.commit()
    return WorkflowResponse(**payload.model_dump())

@router.get("", response_model=list[WorkflowSummary])
def list_workflows(db: Session = Depends(get_db)):
    records = db.scalars(select(WorkflowRecord).order_by(WorkflowRecord.name)).all()
    return [WorkflowSummary(id=r.id, name=r.name, event_count=len(r.events)) for r in records]

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: str, db: Session = Depends(get_db)):
    workflow = to_schema(get_record_or_404(workflow_id, db))
    return WorkflowResponse(**workflow.model_dump())

@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(workflow_id: str, db: Session = Depends(get_db)):
    record = get_record_or_404(workflow_id, db)
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{workflow_id}/analytics", response_model=WorkflowAnalytics)
def get_workflow_analytics(workflow_id: str, db: Session = Depends(get_db)):
    workflow = to_schema(get_record_or_404(workflow_id, db))
    return calculate_analytics(workflow.id, workflow.events)

@router.post("/compare", response_model=WorkflowComparison)
def compare_saved_workflows(payload: WorkflowComparisonRequest, db: Session = Depends(get_db)):
    baseline = to_schema(get_record_or_404(payload.baseline_workflow_id, db))
    candidate = to_schema(get_record_or_404(payload.candidate_workflow_id, db))
    return compare_workflows(baseline, candidate)
