import os
import json
from openai import OpenAI
from app.schemas.category import ProductInput, CategoryOutput

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_product_category(product: ProductInput) -> dict:
    """Takes a sustainable product description and categorizes it using LLM."""
    
    prompt = f"""
    You are an AI Product Categorizer for a sustainable commerce platform.
    Analyze this product:
    Name: {product.product_name}
    Description: {product.description}
    
    Categorize it into one of these primary categories ONLY if applicable:
    Home & Kitchen, Personal Care, Fashion, Food & Beverage, Others.
    
    Provide 5-10 SEO friendly tags, a sub-category, and list sustainability filters.
    Return JSON format strictly matching the schema.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # or gpt-4
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant designed to output strict JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Parse the structured JSON response
        result = json.loads(response.choices[0].message.content)
        
        # Validating using Pydantic (to ensure structure matches)
        validated_result = CategoryOutput(**result)
        
        # To simulate a database store, we log it and return it
        print(f"DEBUG [DB-Sim] -> Saving Category Data: {validated_result.model_dump()}")
        return validated_result.model_dump()
        
    except Exception as e:
        # Simple Error Handling Integration
        raise ValueError(f"AI Category Generation Failed: {str(e)}")
