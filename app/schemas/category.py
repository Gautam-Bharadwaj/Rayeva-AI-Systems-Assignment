from pydantic import BaseModel, Field
from typing import List, Optional

class ProductInput(BaseModel):
    product_name: str = Field(..., description="The name of the product")
    description: str = Field(..., description="Detailed description of the product and its materials")

class CategoryOutput(BaseModel):
    primary_category: str = Field(..., description="Main category from predefined sustainability list")
    sub_category: str = Field(..., description="A granular sub-category based on the product")
    seo_tags: List[str] = Field(..., min_length=5, max_length=10, description="5-10 SEO friendly tags")
    sustainability_filters: List[str] = Field(..., description="Filters like plastic-free, compostable, vegan, recycled")
