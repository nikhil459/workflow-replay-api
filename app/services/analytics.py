from app.schemas.workflow import WorkflowAnalytics, WorkflowEvent

def calculate_analytics(workflow_id: str, events: list[WorkflowEvent]) -> WorkflowAnalytics:
    ordered = sorted(events, key=lambda event: event.timestamp)
    successful = sum(event.status == "success" for event in ordered)
    failed = sum(event.status == "failed" for event in ordered)
    warnings = sum(event.status == "warning" for event in ordered)
    duration = 0.0
    longest_gap = 0.0
    if len(ordered) > 1:
        duration = (ordered[-1].timestamp - ordered[0].timestamp).total_seconds()
        gaps = [(b.timestamp - a.timestamp).total_seconds() for a, b in zip(ordered, ordered[1:])]
        longest_gap = max(gaps, default=0.0)
    return WorkflowAnalytics(
        workflow_id=workflow_id,
        total_events=len(ordered),
        successful_events=successful,
        failed_events=failed,
        warning_events=warnings,
        duration_seconds=duration,
        longest_gap_seconds=longest_gap,
        success_rate=round(successful / len(ordered) * 100, 2),
    )
