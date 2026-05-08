from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import StoreHygieneResponse
from app.services.vision_service import analyze_glow_sign, analyze_branding_compliance, analyze_store_image

router = APIRouter(prefix="/api/v1/store-hygiene", tags=["Store Hygiene"])

@router.post("/analyze", response_model=StoreHygieneResponse)
async def analyze_store(
    store_id: str = Form(...),
    images: list[UploadFile] = File(...)
):
    if not images:
        raise HTTPException(status_code=400, detail="At least one image is required")
    
    all_flags = []
    glow_scores, brand_scores, store_scores = [], [], []
    
    for img_file in images:
        content = await img_file.read()
        
        glow = analyze_glow_sign(content)
        glow_scores.append(glow["score"])
        all_flags.extend(glow["flags"])
        
        brand = analyze_branding_compliance(content)
        brand_scores.append(brand["score"])
        all_flags.extend(brand["flags"])
        
        store = analyze_store_image(content)
        store_scores.append(store["score"])
        all_flags.extend(store["flags"])
    
    avg = lambda lst: round(sum(lst) / len(lst), 1) if lst else 0.0
    
    glow_avg = avg(glow_scores)
    brand_avg = avg(brand_scores)
    store_avg = avg(store_scores)
    overall = round((glow_avg + brand_avg + store_avg) / 3, 1)
    
    return StoreHygieneResponse(
        store_id=store_id,
        glow_sign_score=glow_avg,
        branding_score=brand_avg,
        store_image_score=store_avg,
        overall_score=overall,
        flags=list(set(all_flags)),
        status="processed"
    )