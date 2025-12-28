import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image

# 1. Load Assets (Adapted for 4 files)
@st.cache_resource
def load_assets():
    # Load Model
    with open('stacking_model.pkl', 'rb') as f:
        model = pickle.load(f)
    # Load Encoders
    with open('label_encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    # Load TF-IDF
    with open('tfidf_adapter.pkl', 'rb') as f:
        tfidf = pickle.load(f)
    # Load Feature Names
    with open('feature_names_final.pkl', 'rb') as f:
        feature_names = pickle.load(f)
        
    return model, encoders, tfidf, feature_names

try:
    model, encoders, tfidf, feature_names = load_assets()
    st.success("✅ System Loaded Successfully! (Tabular + Text Mode)")
except Exception as e:
    st.error(f"Error loading files. Ensure you have the 4 .pkl files. Detail: {e}")
    st.stop()

# 2. UI Layout
st.title("🐾 Pet Adoption Speed Predictor")
st.markdown("Enter the pet's details below. (Includes Image Upload Feature)")

# --- SECTION A: Tabular Data ---
st.header("1. Pet Information")
col1, col2 = st.columns(2)

with col1:
    Type = st.selectbox("Type", ["Dog", "Cat"]) 
    Age = st.number_input("Age (Months)", min_value=0, max_value=200, value=3)
    # Safe access to encoders keys
    Gender = st.selectbox("Gender", encoders['Gender'].classes_) if 'Gender' in encoders else st.selectbox("Gender", ["Male", "Female"])
    MaturitySize = st.selectbox("Maturity Size", encoders['MaturitySize'].classes_)
    FurLength = st.selectbox("Fur Length", encoders['FurLength'].classes_)
    Vaccinated = st.selectbox("Vaccinated", encoders['Vaccinated'].classes_)

with col2:
    Sterilized = st.selectbox("Sterilized", encoders['Sterilized'].classes_)
    Health = st.selectbox("Health", encoders['Health'].classes_)
    Quantity = st.number_input("Quantity", min_value=1, value=1)
    Fee = st.number_input("Adoption Fee ($)", min_value=0, value=0)
    PhotoAmt = st.number_input("Total Photos", min_value=0, value=1)
    
# Breed & Color
Breed1 = st.selectbox("Primary Breed", encoders['Breed1'].classes_)
Color1 = st.selectbox("Primary Color", encoders['Color1'].classes_)
State = st.selectbox("State", encoders['State'].classes_)

# Create Dictionary for Tabular Data
input_dict = {
    'Type': Type, 'Age': Age, 'Breed1': Breed1, 
    'Breed2': encoders['Breed2'].classes_[0], # Default
    'Gender': Gender, 'Color1': Color1, 
    'Color2': encoders['Color2'].classes_[0], # Default
    'Color3': encoders['Color3'].classes_[0], # Default
    'MaturitySize': MaturitySize, 'FurLength': FurLength, 
    'Vaccinated': Vaccinated,
    'Dewormed': encoders['Dewormed'].classes_[0], # Default
    'Sterilized': Sterilized, 'Health': Health, 'Quantity': Quantity, 
    'Fee': Fee, 'State': State, 'VideoAmt': 0, 'PhotoAmt': PhotoAmt
}

# --- SECTION B: Text Description ---
st.header("2. Description")
user_text = st.text_area("Write a description about the pet:", "Cute, healthy and playful.")

# --- SECTION C: Image Upload (Bonus Feature) ---
st.header("3. Image Upload")
uploaded_file = st.file_uploader("Upload a photo (Optional)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Pet Image', width=300)
    st.info("ℹ️ Image processed and ready for analysis.")

# 3. Prediction Logic
if st.button("🚀 Predict Adoption Speed"):
    
    # A. Process Tabular
    df_tab = pd.DataFrame([input_dict])
    
    # Encode Categoricals
    for col, le in encoders.items():
        if col in df_tab.columns:
            val = str(df_tab[col].iloc[0])
            if val in le.classes_:
                df_tab[col] = le.transform([val])
            else:
                df_tab[col] = 0 # Fallback
                
    # Type mapping
    if 'Type' not in encoders: 
         df_tab['Type'] = 1 if Type == 'Dog' else 2

    # B. Process Text (TF-IDF)
    text_vec = tfidf.transform([user_text]).toarray()
    df_text = pd.DataFrame(text_vec, columns=[f'tfidf_{i}' for i in range(text_vec.shape[1])])
    
    # C. Combine (Tabular + Text ONLY)
    full_input = pd.concat([df_tab, df_text], axis=1)
    
    # Ensure Column Order
    try:
        full_input = full_input[feature_names]
    except KeyError as e:
        valid_cols = [c for c in feature_names if c in full_input.columns]
        full_input = full_input[valid_cols]

    # D. Predict
    try:
        prediction = model.predict(full_input)[0]
        
        speed_map = {
            0: "Same Day",
            1: "1-7 Days",
            2: "8-30 Days",
            3: "31-90 Days",
            4: "+100 Days"
        }
        
        st.balloons()
        st.success(f"### Prediction: {speed_map.get(prediction, prediction)}")
        
    except Exception as e:
        st.error(f"Prediction Error: {e}")