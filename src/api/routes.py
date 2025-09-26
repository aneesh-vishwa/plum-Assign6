# src/api/routes.py

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional

from src.services import ocr_service, parser_service, risk_engine
from src.services.parser_service import IncompleteProfileError
from src.utils.schemas import HealthProfileResponse, ErrorResponse

router = APIRouter()

@router.post(
    "/profile",
    response_model=HealthProfileResponse,
    responses={
        200: {"model": HealthProfileResponse},
        400: {"model": ErrorResponse}
    }
)
async def create_health_profile(
    survey_text: Optional[str] = Form(None),
    survey_image: Optional[UploadFile] = File(None)
):
    """
    Analyzes lifestyle survey responses from text or an image to generate a
    structured health risk profile.
    """
    if not survey_text and not survey_image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide either 'survey_text' or 'survey_image'."
        )

    raw_text = ""
    if survey_image:
        image_bytes = await survey_image.read()
        raw_text = ocr_service.extract_text_from_image(image_bytes)
    elif survey_text:
        raw_text = survey_text

    try:
        # Step 1: Parse text and apply guardrails
        answers = parser_service.parse_survey_text(raw_text)
        
        # Step 2: Extract factors
        factors = risk_engine.extract_factors(answers)
        
        # Step 3: Risk classification (we only need the level for the final response)
        risk_details = risk_engine.calculate_risk(factors)
        risk_level = risk_details.get("risk_level", "unknown")
        
        # Step 4: Generate recommendations
        recommendations = risk_engine.generate_recommendations(factors)
        
        # Assemble and return the final successful response
        return HealthProfileResponse(
            risk_level=risk_level,
            factors=factors,
            recommendations=recommendations
        )
        
    except IncompleteProfileError as e:
        # Handle the specific guardrail error from the parser
        error_payload = ErrorResponse(status="incomplete_profile", reason=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_payload.dict()
        )
    except Exception as e:
        # Handle other potential errors gracefully
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )