from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import GroomingResponse, ActionInput, ActionsResponse, TaggedAction
from app.services.vision_service import analyze_grooming
from app.services.nlp_service import tag_action, score_actions

router = APIRouter(prefix="/api/v1/champion", tags=["Champion Development"])

@router.post("/grooming-check", response_model=GroomingResponse)
async def grooming_check(
    champion_id: str = Form(...),
    photo: UploadFile = File(...)
):
    content = await photo.read()
    result = analyze_grooming(content)
    
    return GroomingResponse(
        champion_id=champion_id,
        grooming_score=result["score"],
        flags=result["flags"],
        compliant=result["compliant"]
    )

@router.post("/actions-score", response_model=ActionsResponse)
async def actions_score(body: ActionInput):
    if not body.actions:
        raise HTTPException(status_code=400, detail="Actions list cannot be empty")
    
    tagged = []
    for action in body.actions:
        result = tag_action(action)
        tagged.append(TaggedAction(
            action=action,
            tag=result["tag"],
            confidence=result["confidence"]
        ))
    
    overall_score = score_actions(body.actions)
    
    return ActionsResponse(
        champion_id=body.champion_id,
        actions_score=overall_score,
        tagged_actions=tagged
    )