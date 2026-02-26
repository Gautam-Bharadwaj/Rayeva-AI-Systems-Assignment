from fastapi import APIRouter, HTTPException
from app.schemas.category import ProductInput, CategoryOutput
from app.services.ai import generate_product_category

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
