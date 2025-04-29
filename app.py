import streamlit as st
import joblib
import pandas as pd


model = joblib.load('model_gb.pkl')


st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="centered")


st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .title {
            font-size: 2.5em;
            font-weight: 700;
            color: #2A2F4F;
            text-align: center;
            padding: 20px;
            background: linear-gradient(45deg, #2A2F4F, #7B68EE);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 20px 0;
        }
        
        .card {
            background: #FFFFFF;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 15px 0;
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .stNumberInput, .stSelectbox {
            margin: 10px 0;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #2A2F4F 0%, #7B68EE 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
            background: linear-gradient(135deg, #7B68EE 0%, #2A2F4F 100%);
        }
        
        .result-box {
            background: linear-gradient(135deg, #2A2F4F, #7B68EE);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .feature-icon {
            font-size: 1.2em;
            margin-right: 8px;
            vertical-align: middle;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title">Estimation Intelligente de Prix Immobilier 🏡</h1>', unsafe_allow_html=True)
st.markdown('Pour avoir les détails du code vous pouvez cliquez sur ce lien: https://github.com/kadidiatousow/prediction-des-prix-immobilier')

with st.form("prediction_form"):
    with st.container():
        st.markdown("### 📋 Caractéristiques du Bien")
        col1, col2 = st.columns(2)
        
        with col1:
            bedrooms = st.number_input("🛏 Nombre de chambres", min_value=1, max_value=10, value=3)
            bathrooms = st.number_input("🚿 Nombre de salles de bain", min_value=1, max_value=5, value=2)
            sqft_living = st.number_input("📏 Surface habitable (sqft)", min_value=500, max_value=10000, value=2000)
            sqft_lot = st.number_input("🌳 Surface du terrain (sqft)", min_value=500, max_value=100000, value=5000)
            
        with col2:
            floors = st.number_input("🏢 Nombre d'étages", min_value=1, max_value=5, value=2)
            waterfront = st.selectbox("🌊 Vue sur l'eau", ["Non", "Oui"])
            view = st.selectbox("🌆 Vue (qualité)", [0, 1, 2, 3, 4])
            condition = st.selectbox("⚡ État du bien", ["Mauvais", "Moyen", "Excellent"])
    
    
    waterfront = 1 if waterfront == "Oui" else 0
    condition_mapping = {"Mauvais": 0, "Moyen": 1, "Excellent": 2}
    condition = condition_mapping[condition]
    
   
    user_data = pd.DataFrame({
        'bedrooms': [bedrooms],
        'bathrooms': [bathrooms],
        'sqft_living': [sqft_living],
        'sqft_lot': [sqft_lot],
        'floors': [floors],
        'waterfront': [waterfront],
        'view': [view],
        'condition': [condition],
        'grade': [7], 
        'sqft_above': [sqft_living],  
        'sqft_basement': [0],  
        'yr_built': [2000],  
        'yr_renovated': [0], 
        'zipcode': [98001],  
        'lat': [47.5112],  
        'long': [-122.257],
        'sqft_living15': [sqft_living], 
        'sqft_lot15': [sqft_lot]
    })
    
    
    submitted = st.form_submit_button("📈 Obtenir l'Estimation")


if submitted:
    try:
        prediction = model.predict(user_data)
        st.markdown(f"""
            <div class="result-box">
                <h3 style="text-align:center; margin:0">
                    Estimation du Prix :<br>
                    <span style="font-size:1.5em; color:#FFD700">${prediction[0]:,.2f}</span>
                </h3>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")

