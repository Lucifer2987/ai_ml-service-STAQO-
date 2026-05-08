from pydantic import BaseModel
from typing import Optional

class StoreHygieneResponse(BaseModel):
    store_id: str
    glow_sign_score: float
    branding_score: float
    store_image_score: float
    overall_score: float
    flags: list[str]
    status: str

class GroomingResponse(BaseModel):
    champion_id: str
    grooming_score: float
    flags: list[str]
    compliant: bool

class ActionInput(BaseModel):
    champion_id: str
    actions: list[str]

class TaggedAction(BaseModel):
    action: str
    tag: str  # "compliant", "training_required", "non_compliant", "in_progress"
    confidence: float

class ActionsResponse(BaseModel):
    champion_id: str
    actions_score: float
    tagged_actions: list[TaggedAction]

class ChatInput(BaseModel):
    question: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    source: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str