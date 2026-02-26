from fastapi import APIRouter, HTTPException
from app.schemas.category import ProductInput, CategoryOutput
from app.services.ai import generate_product_category

from app.schemas.impact import OrderInput, ImpactOutput
from app.services.impact_ai import calculate_impact_and_generate_report

router = APIRouter()

@router.post("/module1/categorize", response_model=CategoryOutput, summary="Auto-Category & Tag Generator")
async def categorize_product(product: ProductInput):
    """
    Takes a product description and Auto-assigns:
    1. Primary Category
    2. Sub-category
    3. 5-10 SEO tags
    4. Sustainability filters
    Returns structured JSON and simulates DB storage.
    """
    try:
        # Calls the AI service logic, returning a validated dictionary matching the DB schema
        result = generate_product_category(product)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error during AI computation")

@router.post("/module3/impact", response_model=ImpactOutput, summary="AI Impact Reporting Generator")
async def generate_impact_report(order: OrderInput):
    """
    Takes an order and estimates:
    1. Plastic saved (business logic)
    2. Carbon avoided (business logic)
    3. Local sourcing impact summary (AI Generated)
    4. Human-readable impact statement (AI Generated)
    Combines them into structured JSON.
    """
    try:
        result = calculate_impact_and_generate_report(order)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error during Impact computation")

