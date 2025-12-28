# Pet Adoption Speed Prediction (XAI & Multi-Modal Fusion)

This project predicts the adoption speed of shelter pets using a combination of **Tabular**, **Textual**, and **Visual** data. By leveraging advanced Machine Learning and Explainable AI (XAI), we identify the key factors that help pets find their forever homes faster.

## Key Features

* **Multi-Modal Fusion:** Combines structured metadata, semantic text embeddings (FastText), and deep learning image features (EfficientNet).
* **Champion Model:** Utilizes a highly tuned **XGBoost** classifier within a stacking ensemble.
* **Explainable AI (XAI):** Integrated **SHAP (Permutation Explainer)** to provide transparent insights into the model's decision-making process.
* **Dockerized Deployment:** Fully containerized **Streamlit** application for easy testing and deployment.

---

## Modality Analysis (Ablation Study)

We conducted an extensive study to evaluate the contribution of each data type:

| Modality Combination | Num Features | Avg K-Fold QWK |
| --- | --- | --- |
| **Tabular + Text** | **131** | **0.3401 (Winner)** |
| Tabular Only | 31 | 0.3376 |
| All Features (Fusion) | 1411 | 0.3312 |

**Insight:** While image features provide depth, the **Tabular + Text** combination offered the most robust performance, proving that the "story" (description) and metadata are the strongest predictors.

---

## Installation & Usage

### Option 1: Running with Docker (Recommended)

Ensure you have Docker Desktop installed.

1. **Build the Image:**
```bash
docker build -t pet-adoption-app .

```


2. **Run the Container:**
```bash
docker run -p 8501:8501 pet-adoption-app

```


3. **Access the App:** Open `http://localhost:8501` in your browser.

### Option 2: Running with Python

1. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


2. **Run Streamlit:**
```bash
python -m streamlit run app.py --server.port 8501

```



---

## Model Interpretation (XAI)

We use **SHAP** to understand the "Why" behind each prediction:

* **Age:** Younger animals have a significantly higher adoption speed.
* **Semantic Quality:** The narrative quality of the pet's description (extracted via FastText) plays a crucial role.
* **Medical Readiness:** Vaccinated and sterilized status are key trust indicators for adopters.

---

## App Preview

* **User Friendly:** Input pet details and descriptions to get an instant prediction.
* **Optional Images:** The app is optimized to work even without image uploads, prioritizing the most predictive features.
* **Real-time Analytics:** Visualizes which factors in your specific input increased or decreased the adoption speed.

---

## Project Structure

```text
.
├── app.py                      # Main Streamlit application
├── requirements.txt             # Python dependencies
├── Dockerfile                  # Docker configuration
├── petfinder-project-notebook.ipynb   # Data analysis & training notebook
├── final_model.pkl             # Trained XGBoost/Stacking model
├── scaler.pkl                  # StandardScaler for numerical features
├── label_encoders.pkl          # Categorical encoders
├── imputer.pkl                 # Missing value handler
└── fasttext_model.bin          # FastText model for description embeddings

