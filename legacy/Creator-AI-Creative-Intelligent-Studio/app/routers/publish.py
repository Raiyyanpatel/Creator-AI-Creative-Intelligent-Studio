import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path

from app.models.publish import (
    PublishCreateRequest,
    HumanApprovalRequest,
    HumanRejectionRequest,
    PublishJob,
    PublishResponse
)
from app.services.composio_service import composio_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publish", tags=["Composio Publishing & Human Approval"])

@router.post("", response_model=PublishResponse, summary="Submit content for publishing with Human Approval & Composio")
@router.post("/request", response_model=PublishResponse, summary="Submit content for publishing with Human Approval & Composio")
def submit_publish_request(req: PublishCreateRequest):
    """
    Submits a post, short, video, or article to be published to YouTube, LinkedIn, X/Twitter, or Substack.
    Enforces a strict Human-In-The-Loop approval gate: sets status to 'PENDING_APPROVAL'
    and prepares the Composio toolset execution payload.
    """
    logger.info(f"Received publish request for {req.creator_id} on {req.platform} ({req.content_format})")
    job = composio_service.create_publish_job(req)
    
    msg = (
        f"Publish job {job.job_id} created successfully and is WAITING FOR HUMAN APPROVAL. "
        f"Call POST /publish/jobs/{job.job_id}/approve to approve and dispatch via Composio."
        if job.status == "PENDING_APPROVAL"
        else f"Publish job {job.job_id} dispatched immediately via Composio."
    )

    return PublishResponse(
        status="success",
        message=msg,
        job=job
    )

@router.get("/jobs", response_model=List[PublishJob], summary="List all publish jobs and approval queue")
def list_publish_jobs(
    creator_id: Optional[str] = Query(None, description="Filter by creator identifier"),
    status: Optional[str] = Query(None, description="Filter by status: 'PENDING_APPROVAL', 'APPROVED', 'PUBLISHED', 'REJECTED'")
):
    """
    Returns the queue of publishing jobs. Used by the React Native app to display the
    'Pending Approvals' feed and publishing history.
    """
    return composio_service.list_jobs(creator_id=creator_id, status=status)

@router.get("/jobs/{job_id}", response_model=PublishJob, summary="Get details and approval status of a publish job")
def get_publish_job(job_id: str = Path(..., description="Unique publish job ID")):
    job = composio_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return job

@router.post("/jobs/{job_id}/approve", response_model=PublishResponse, summary="Human Approval: Authorize & trigger Composio publication")
def approve_publish_job(
    job_id: str = Path(..., description="Job ID to approve"),
    approval: HumanApprovalRequest = HumanApprovalRequest()
):
    """
    Human-in-the-loop approval step. Authorizes content dispatch, records reviewer feedback,
    and immediately invokes Composio's real platform tools to publish the content live.
    """
    try:
        job = composio_service.approve_publish_job(job_id, approval)
        return PublishResponse(
            status="success",
            message=f"Job {job_id} approved by {approval.reviewer_name} and successfully published via Composio!",
            job=job
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error approving job {job_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to publish via Composio: {str(e)}")

@router.post("/jobs/{job_id}/reject", response_model=PublishResponse, summary="Human Rejection: Reject proposed content")
def reject_publish_job(
    job_id: str = Path(..., description="Job ID to reject"),
    rejection: HumanRejectionRequest = HumanRejectionRequest(rejection_reason="Tone mismatch")
):
    """
    Human rejection step. Cancels publication and saves feedback so the AI can refine future drafts.
    """
    try:
        job = composio_service.reject_publish_job(job_id, rejection)
        return PublishResponse(
            status="success",
            message=f"Job {job_id} has been rejected by human reviewer.",
            job=job
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
