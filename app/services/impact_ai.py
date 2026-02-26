import os
import json
from openai import OpenAI
from app.schemas.impact import OrderInput, ImpactOutput

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

def calculate_impact_and_generate_report(order: OrderInput) -> dict:
    # 1. Business Logic Estimation
    plastic_g_per_item = 15
    carbon_kg_per_local_item = 0.5
    
    total_plastic_saved = sum([item.quantity * plastic_g_per_item for item in order.items if item.is_plastic_free])
    total_carbon_avoided = sum([item.quantity * carbon_kg_per_local_item for item in order.items if item.is_locally_sourced])
    local_items_count = sum([item.quantity for item in order.items if item.is_locally_sourced])
    
    # Let AI craft a personalized story based on this logic
    prompt = f"""
    An eco-conscious order ({order.order_id}) was just placed.
    - Plastic avoided: {total_plastic_saved}g
    - Carbon emissions avoided (local sourcing): {total_carbon_avoided} kg
    - Total items sourced locally: {local_items_count}
    
    Generate a short summary on local sourcing impact, and a creative, human-readable impact statement to print on their receipt or email.
    The response MUST strictly be a JSON object containing:
    "local_sourcing_summary" (string), "human_readable_impact_statement" (string).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a Sustainability Impact Reporter. Output strict JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Merge business logic metrics + AI generated text mapping to ImpactOutput Schema
        final_doc = {
            "order_id": order.order_id,
            "estimated_plastic_saved_grams": total_plastic_saved,
            "carbon_avoided_kg": total_carbon_avoided,
            "local_sourcing_summary": result.get("local_sourcing_summary", ""),
            "human_readable_impact_statement": result.get("human_readable_impact_statement", "")
        }
        
        # Validate through Pydantic
        validated_result = ImpactOutput(**final_doc)
        print(f"DEBUG [DB-Sim] -> Storing Order Impact Logs: {validated_result.model_dump()}")
        return validated_result.model_dump()
        
    except Exception as e:
        raise ValueError(f"AI Impact Generation Failed: {str(e)}")
