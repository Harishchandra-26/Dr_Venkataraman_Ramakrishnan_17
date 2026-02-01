import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    np.random.seed(42)

    cities = [
        'Mumbai','Delhi','Chennai','Kolkata','Bangalore',
        'Hyderabad','Ahmedabad','Pune','Jaipur','Lucknow'
    ]

    data = []
    for city in cities:
        for _ in range(50):
            rainfall = np.random.uniform(0, 200)
            drainage = np.random.randint(1, 6)
            contamination = np.random.uniform(0, 100)
            sanitation = np.random.uniform(20, 100)
            temp = np.random.uniform(25, 40)
            humidity = np.random.uniform(40, 95)
            density = np.random.randint(5000, 50000)
            historical = np.random.randint(0, 5)

            risk_score = (
                rainfall/200 * 0.2 +
                (drainage-1)/4 * 0.25 +
                contamination/100 * 0.25 +
                (100-sanitation)/100 * 0.15 +
                humidity/100 * 0.1 +
                min(density/50000, 1) * 0.05
            )

            outbreak = 1 if risk_score > 0.65 else 0

            disease = 'None'
            if outbreak:
                disease = np.random.choice(
                    ['Cholera','Typhoid','Diarrhea','Hepatitis A']
                )

            if risk_score < 0.3:
                risk_cat = 'Low'
            elif risk_score < 0.6:
                risk_cat = 'Medium'
            elif risk_score < 0.8:
                risk_cat = 'High'
            else:
                risk_cat = 'Critical'

            data.append({
                'date': (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d'),
                'city': city,
                'rainfall_mm': round(rainfall,1),
                'drainage_score': drainage,
                'population_density': density,
                'water_contamination': round(contamination,1),
                'sanitation_coverage': round(sanitation,1),
                'temperature_c': round(temp,1),
                'humidity_percent': round(humidity,1),
                'historical_outbreaks': historical,
                'risk_score': round(risk_score,3),
                'outbreak_prediction': outbreak,
                'predicted_disease': disease,
                'risk_category': risk_cat,
                'latitude': np.random.uniform(8.0, 33.0),
                'longitude': np.random.uniform(68.0, 97.0)
            })

    return pd.DataFrame(data)


def categorize_risk(risk_score):
    if risk_score < 0.3:
        return 'Low', 'green', '🟢'
    elif risk_score < 0.6:
        return 'Medium', 'yellow', '🟡'
    elif risk_score < 0.8:
        return 'High', 'orange', '🟠'
    else:
        return 'Critical', 'red', '🔴'
