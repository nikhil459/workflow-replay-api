from app.schemas.workflow import WorkflowComparison, WorkflowCreate
from app.services.analytics import calculate_analytics

def compare_workflows(baseline: WorkflowCreate, candidate: WorkflowCreate) -> WorkflowComparison:
    base = calculate_analytics(baseline.id, baseline.events)
    cand = calculate_analytics(candidate.id, candidate.events)
    base_types = {event.type for event in baseline.events}
    cand_types = {event.type for event in candidate.events}
    return WorkflowComparison(
        baseline_workflow_id=baseline.id,
        candidate_workflow_id=candidate.id,
        duration_difference_seconds=cand.duration_seconds - base.duration_seconds,
        event_count_difference=cand.total_events - base.total_events,
        failed_event_difference=cand.failed_events - base.failed_events,
        missing_event_types=sorted(base_types - cand_types),
        additional_event_types=sorted(cand_types - base_types),
    )
