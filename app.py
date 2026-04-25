from flask import Flask, render_template, request, jsonify, session
from firebase_config import save_user, save_carbon_data, get_user_history, get_leaderboard, update_points
from ai_engine import predict_carbon_footprint, get_chatbot_response, generate_report_summary, calculate_manual
from fpdf import FPDF
import os
import json

app = Flask(__name__)
app.secret_key = 'carboniq-hackathon-2024'

# ============================================
# ROUTES - Pages
# ============================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/report')
def report():
    return render_template('report.html')

# ============================================
# API ROUTES - Backend Logic
# ============================================

@app.route('/api/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    try:
        save_user(data)
        session['user_email'] = data['email']
        session['user_name'] = data['name']
        return jsonify({'status': 'success', 'message': 'User registered!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate carbon footprint using AI prediction"""
    data = request.json
    
    try: 
        # AI Prediction - This is the STANDOUT feature!
        prediction = predict_carbon_footprint(data)
        
        # Save to Firebase
        email = session.get('user_email', 'anonymous')
        carbon_record = {
            'transport': prediction.get('transport_co2', 0),
            'energy': prediction.get('energy_co2', 0),
            'food': prediction.get('food_co2', 0),
            'shopping': prediction.get('shopping_co2', 0),
            'waste': prediction.get('waste_co2', 0),
            'total': prediction.get('total_kg_co2_per_month', 0),
            'prediction': prediction.get('rating', ''),
            'tips': prediction.get('personalized_tips', [])
        }
        
        try:
            save_carbon_data(email, carbon_record)
            # Award green points
            points = max(0, 100 - int(prediction.get('total_kg_co2_per_month', 0) / 10))
            update_points(email, points)
            prediction['points_earned'] = points
        except:
            prediction['points_earned'] = 0
        
        return jsonify({'status': 'success', 'data': prediction})
    
    except Exception as e:
        # Fallback to manual calculation
        fallback = calculate_manual(data)
        return jsonify({'status': 'success', 'data': fallback})

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI Chatbot endpoint"""
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', '')
    
    response = get_chatbot_response(user_message, context)
    return jsonify({'status': 'success', 'response': response})

@app.route('/api/history', methods=['GET'])
def history():
    """Get user history"""
    email = session.get('user_email', 'anonymous')
    try:
        data = get_user_history(email)
        return jsonify({'status': 'success', 'data': data})
    except:
        return jsonify({'status': 'success', 'data': []})

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard_api():
    """Get leaderboard"""
    try:
        data = get_leaderboard()
        return jsonify({'status': 'success', 'data': data})
    except:
        return jsonify({'status': 'success', 'data': []})

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate PDF report"""
    data = request.json
    
    try:
        # Get AI summary
        summary = generate_report_summary(data)
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 20, 'CarbonIQ Report', ln=True, align='C')
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Total Carbon Footprint: {data.get('total_kg_co2_per_month', 'N/A')} kg CO2/month", ln=True)
        pdf.cell(0, 10, f"Rating: {data.get('rating', 'N/A')}", ln=True)
        pdf.cell(0, 10, f"Yearly Projection: {data.get('yearly_projection', 'N/A')} kg CO2", ln=True)
        pdf.cell(0, 10, f"Trees Needed to Offset: {data.get('trees_needed', 'N/A')}", ln=True)
        
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Breakdown:', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f"Transport: {data.get('transport_co2', 0)} kg CO2", ln=True)
        pdf.cell(0, 8, f"Energy: {data.get('energy_co2', 0)} kg CO2", ln=True)
        pdf.cell(0, 8, f"Food: {data.get('food_co2', 0)} kg CO2", ln=True)
        pdf.cell(0, 8, f"Shopping: {data.get('shopping_co2', 0)} kg CO2", ln=True)
        pdf.cell(0, 8, f"Waste: {data.get('waste_co2', 0)} kg CO2", ln=True)
        
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'AI Analysis:', ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 7, summary)
        
        # Save PDF
        pdf_path = os.path.join('static', 'reports', 'carbon_report.pdf')
        os.makedirs(os.path.join('static', 'reports'), exist_ok=True)
        pdf.output(pdf_path)
        
        return jsonify({'status': 'success', 'pdf_url': '/' + pdf_path})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)