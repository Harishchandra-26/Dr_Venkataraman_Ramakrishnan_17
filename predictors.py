from datetime import datetime
from data_simulation import categorize_risk

def predict_outbreak_simple(input_data):
    risk_score = (
        input_data.get('rainfall_mm', 0)/200 * 0.2 +
        (input_data.get('drainage_score', 1)-1)/4 * 0.25 +
        input_data.get('water_contamination', 0)/100 * 0.25 +
        (100-input_data.get('sanitation_coverage', 100))/100 * 0.15 +
        input_data.get('humidity_percent', 50)/100 * 0.1 +
        min(input_data.get('population_density', 10000)/50000, 1) * 0.05
    )

    if datetime.now().month in [6,7,8,9]:
        risk_score *= 1.3

    probability = min(risk_score * 1.2, 0.95)
    outbreak = 1 if probability > 0.65 else 0

    category, color, emoji = categorize_risk(risk_score)

    disease = 'None'
    if outbreak:
        if input_data.get('water_contamination',0) > 60:
            disease = 'Cholera'
        elif input_data.get('sanitation_coverage',100) < 50:
            disease = 'Diarrhea'
        elif input_data.get('temperature_c',30) > 35:
            disease = 'Typhoid'

    return {
        'outbreak': outbreak,
        'probability': probability,
        'risk_score': risk_score,
        'category': category,
        'color': color,
        'emoji': emoji,
        'disease': disease,
        'confidence': 'High' if probability > 0.8 else 'Medium'
    }


def generate_recommendations(prediction, input_data):
    recs = []

    if prediction['outbreak']:
        recs.append("🚨 IMMEDIATE ACTION REQUIRED")
        recs.append("• Emergency water treatment")
        recs.append("• Drainage cleanup")
        recs.append("• Medical readiness")
    else:
        recs.append("✅ Preventive monitoring")
        recs.append("• Regular water testing")
        recs.append("• Sanitation awareness")

    return recs
