import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def get_ai_response(prompt):
    """Get response from Ollama AI"""
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response']
    except Exception as e:
        return f"AI is currently unavailable: {str(e)}"

def predict_carbon_footprint(user_data):
    """
    AI PREDICTION MODEL
    Uses AI to analyze ALL factors and predict carbon footprint
    """
    prompt = f"""
    You are a carbon footprint prediction AI expert. Analyze the following user data 
    and provide a detailed carbon footprint prediction.

    USER DATA:
    - Daily car travel: {user_data.get('car_km', 0)} km
    - Car type: {user_data.get('car_type', 'petrol')}
    - Daily bike/motorcycle travel: {user_data.get('bike_km', 0)} km
    - Public transport usage: {user_data.get('public_transport_km', 0)} km
    - Flights per year: {user_data.get('flights_per_year', 0)}
    - Monthly electricity bill: ${user_data.get('electricity_bill', 0)}
    - Electricity source: {user_data.get('electricity_source', 'grid')}
    - Gas usage (cooking/heating): {user_data.get('gas_usage', 'moderate')}
    - Diet type: {user_data.get('diet', 'mixed')}
    - Meals with meat per week: {user_data.get('meat_meals', 0)}
    - Food waste per week: {user_data.get('food_waste', 'moderate')}
    - Online shopping orders per month: {user_data.get('shopping_orders', 0)}
    - Clothing purchases per month: {user_data.get('clothing', 0)}
    - Recycling habits: {user_data.get('recycling', 'sometimes')}
    - Home size: {user_data.get('home_size', 'medium')}
    - Number of people in home: {user_data.get('household_members', 1)}
    - AC/Heating usage hours: {user_data.get('ac_hours', 0)}
    - Screen time (devices): {user_data.get('screen_hours', 0)} hours

    RESPOND IN THIS EXACT JSON FORMAT:
    {{
        "total_kg_co2_per_month": <number>,
        "transport_co2": <number>,
        "energy_co2": <number>,
        "food_co2": <number>,
        "shopping_co2": <number>,
        "waste_co2": <number>,
        "lifestyle_co2": <number>,
        "rating": "<Excellent/Good/Average/Poor/Critical>",
        "percentile": "<Better than X% of people>",
        "yearly_projection": <number>,
        "trees_needed": <number to offset>,
        "top_3_issues": ["issue1", "issue2", "issue3"],
        "personalized_tips": [
            "tip1",
            "tip2", 
            "tip3",
            "tip4",
            "tip5"
        ],
        "reduction_potential": "<X% reduction possible>",
        "equivalent": "<equivalent comparison like X flights>"
    }}
    
    Only respond with the JSON, nothing else.
    """
    
    response = get_ai_response(prompt)
    
    try:
        # Try to parse JSON from response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            result = json.loads(response[json_start:json_end])
            return result
    except json.JSONDecodeError:
        pass
    
    # Fallback calculation if AI parsing fails
    return calculate_manual(user_data)

def calculate_manual(data):
    """Fallback manual calculation with emission factors"""
    transport = (
        data.get('car_km', 0) * 0.21 * 30 +
        data.get('bike_km', 0) * 0.05 * 30 +
        data.get('public_transport_km', 0) * 0.089 * 30 +
        data.get('flights_per_year', 0) * 255 / 12
    )
    
    energy = (
        data.get('electricity_bill', 0) * 0.5 +
        data.get('ac_hours', 0) * 1.5 * 30 +
        data.get('screen_hours', 0) * 0.05 * 30
    )
    
    diet_factors = {'vegan': 0.5, 'vegetarian': 0.7, 'mixed': 1.0, 'heavy_meat': 1.5}
    food = (
        data.get('meat_meals', 0) * 7.0 * 4 +
        diet_factors.get(data.get('diet', 'mixed'), 1.0) * 100
    )
    
    shopping = (
        data.get('shopping_orders', 0) * 5.0 +
        data.get('clothing', 0) * 25.0
    )
    
    waste_factors = {'always': 0.5, 'sometimes': 1.0, 'never': 2.0}
    waste = waste_factors.get(data.get('recycling', 'sometimes'), 1.0) * 50
    
    total = transport + energy + food + shopping + waste
    
    return {
        "total_kg_co2_per_month": round(total, 2),
        "transport_co2": round(transport, 2),
        "energy_co2": round(energy, 2),
        "food_co2": round(food, 2),
        "shopping_co2": round(shopping, 2),
        "waste_co2": round(waste, 2),
        "lifestyle_co2": 0,
        "rating": "Excellent" if total < 200 else "Good" if total < 400 else "Average" if total < 600 else "Poor",
        "yearly_projection": round(total * 12, 2),
        "trees_needed": round(total * 12 / 22, 1),
        "top_3_issues": ["Transport", "Energy", "Food"],
        "personalized_tips": [
            "Use public transport more",
            "Switch to renewable energy",
            "Reduce meat consumption",
            "Buy less fast fashion",
            "Start composting"
        ],
        "reduction_potential": "30%",
        "equivalent": f"Equal to {round(total * 12 / 255, 1)} flights per year"
    }

def get_chatbot_response(user_message, context=""):
    """AI Chatbot for carbon-related questions"""
    prompt = f"""
    You are CarbonIQ AI Assistant - a friendly, knowledgeable expert on carbon 
    footprint, climate change, and sustainability. 
    
    User's carbon context: {context}
    
    User asks: {user_message}
    
    Provide a helpful, concise, and actionable response. Use emojis to make it 
    engaging. Keep response under 200 words.
    """
    return get_ai_response(prompt)

def generate_report_summary(carbon_data):
    """Generate AI summary for PDF report"""
    prompt = f"""
    Generate a professional summary report for this carbon footprint data:
    {json.dumps(carbon_data, indent=2)}
    
    Include:
    1. Overall assessment (2-3 sentences)
    2. Key findings
    3. Actionable recommendations
    4. Monthly and yearly impact
    
    Keep it professional and under 300 words.
    """
    return get_ai_response(prompt)