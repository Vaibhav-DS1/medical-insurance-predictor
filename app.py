import streamlit as st
import numpy as np
import joblib
import config

# ===== Load model and metadata =====
@st.cache_resource
def load_model():
    model = joblib.load(config.MODEL_FILE_PATH)
    json_data = {
        'sex': {'male': 1, 'female': 0},
        'smoker': {'yes': 1, 'no': 0},
        'columns': ['age', 'sex', 'bmi', 'children', 'smoker',
                    'region_northeast', 'region_northwest', 'region_southeast', 'region_southwest']
    }
    return model, json_data

model, json_data = load_model()

# ===== Prediction Logic =====
def predict_charges(age, sex, bmi, children, smoker, region):
    region_col = f"region_{region.lower()}"
    
    test_array = np.zeros(len(json_data["columns"]))
    test_array[0] = age
    test_array[1] = json_data["sex"][sex]
    test_array[2] = bmi
    test_array[3] = children
    test_array[4] = json_data["smoker"][smoker]
    
    if region_col in json_data["columns"]:
        region_index = json_data["columns"].index(region_col)
        test_array[region_index] = 1
    else:
        raise ValueError(f"Unknown region: {region}")

    prediction = model.predict([test_array])[0]
    return round(prediction, 2)

# ===== Streamlit UI =====
st.title("🏥 Medical Insurance Charges Predictor")

age = st.slider("Age", 18, 100, 30)
sex = st.selectbox("Sex", ["male", "female"])
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
children = st.slider("Number of Children", 0, 5, 0)
smoker = st.selectbox("Smoker?", ["yes", "no"])
region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

if st.button("Predict Charges"):
    try:
        result = predict_charges(age, sex, bmi, children, smoker, region)
        st.success(f"💰 Estimated Charges: ₹ {result}")
    except Exception as e:
        st.error(f"Error: {e}")
