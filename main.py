from fastapi import FastAPI
from schemas import UserInput
import pickle
import re
from scipy.sparse import hstack

# Load the ML model bundle
with open('ml_model/transaction_categorizer.pkl', 'rb') as f:
    bundle = pickle.load(f)

model = bundle['model']
vectorizer = bundle['vectorizer']
encoder = bundle['encoder']
feature_columns = bundle['feature_columns']

app = FastAPI()


@app.post('/predict')
def predict_category(user_input: UserInput):
    # Preprocess description: lowercase and remove non-alphabetic chars
    desc = re.sub(r'[^a-zA-Z ]', '', user_input.transaction_description.lower())

    # Create one-hot encoded features matching training data structure
    numeric_features = [
        1 if user_input.country == col.replace('country_', '') else 0
        for col in feature_columns if col.startswith('country_')
    ] + [
        1 if user_input.currency == col.replace('currency_', '') else 0
        for col in feature_columns if col.startswith('currency_')
    ]

    import numpy as np
    from scipy.sparse import csr_matrix

    numeric_features_np = np.array(numeric_features).reshape(1, -1)
    numeric_features_sparse = csr_matrix(numeric_features_np)

    # Vectorize description and combine with numeric features
    desc_vec = vectorizer.transform([desc])
    X = hstack([desc_vec, numeric_features_sparse])

    # Predict and decode
    pred = model.predict(X)
    category = encoder.inverse_transform(pred)[0]

    return {"predicted_category": category}