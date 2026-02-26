from pydantic import BaseModel, Field
from typing import List, Optional

class ProductItem(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Number of items ordered")
    is_plastic_free: bool = Field(False, description="Whether the item replaced plastic")
    is_locally_sourced: bool = Field(False, description="Whether it was sourced locally")

class OrderInput(BaseModel):
    order_id: str = Field(..., description="Unique ID for the order")
    items: List[ProductItem] = Field(..., description="List of sustainable products in the order")
    total_amount: float = Field(..., description="Total cost of the order")

class ImpactOutput(BaseModel):
    order_id: str = Field(..., description="ID of the order")
    estimated_plastic_saved_grams: int = Field(..., description="Estimated grams of plastic saved")
    carbon_avoided_kg: float = Field(..., description="Estimated kg of carbon footprint avoided")
    local_sourcing_summary: str = Field(..., description="Summary of local sourcing impact")
    human_readable_impact_statement: str = Field(..., description="A short engaging statement to show the customer")
