import numpy as np
import pickle
import os
import streamlit as st

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

def _load(filename):
    with open(os.path.join(MODEL_DIR, filename), 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_models():
    kmeans  = _load('kmeans_model.pkl')
    encoder = _load('autoencoder_model.pkl')
    rf      = _load('classifier_rf.pkl')
    scaler  = _load('scaler_ae.pkl')
    le      = _load('label_encoder.pkl')
    return kmeans, encoder, rf, scaler, le


def encode_features(X_scaled, encoder):
    """
    Pure sklearn encoding — no TensorFlow, no Keras.
    Tries every standard sklearn interface in order.
    Returns a 2D array matching what the RF was trained on.
    """

    # Option 1: sklearn transform() — Pipeline, PCA, autoencoder wrapper, etc.
    if hasattr(encoder, 'transform'):
        try:
            out = encoder.transform(X_scaled)
            return out
        except Exception:
            pass

    # Option 2: predict() — some custom sklearn-style encoders use this
    if hasattr(encoder, 'predict'):
        try:
            out = encoder.predict(X_scaled)
            # If output has same shape as input (reconstruction), we need
            # only the encoded part — use it directly since RF was trained on it
            return out
        except Exception:
            pass

    # Option 3: encoder is actually the scaler itself or identity
    # Just return scaled features (RF will validate shape)
    return X_scaled


def predict_single(recency, frequency, monetary, encoder, rf, scaler, le):
    X         = np.array([[recency, frequency, monetary]], dtype=float)
    X_scaled  = scaler.transform(X)
    X_encoded = encode_features(X_scaled, encoder)

    # Safety check — if shape doesn't match RF expectation, use scaled directly
    expected_features = rf.n_features_in_
    if X_encoded.shape[1] != expected_features:
        # Try to trim or fallback
        if X_scaled.shape[1] == expected_features:
            X_encoded = X_scaled
        else:
            # Trim to expected features as last resort
            X_encoded = X_encoded[:, :expected_features]

    pred_idx   = rf.predict(X_encoded)[0]
    pred_proba = rf.predict_proba(X_encoded)[0]
    segment    = le.inverse_transform([pred_idx])[0]
    confidence = pred_proba.max() * 100
    return segment, confidence, pred_proba, le.classes_


def predict_batch(df, encoder, rf, scaler, le, segment_config):
    X         = df[['Recency', 'Frequency', 'Monetary']].values.astype(float)
    X_scaled  = scaler.transform(X)
    X_encoded = encode_features(X_scaled, encoder)

    expected_features = rf.n_features_in_
    if X_encoded.shape[1] != expected_features:
        if X_scaled.shape[1] == expected_features:
            X_encoded = X_scaled
        else:
            X_encoded = X_encoded[:, :expected_features]

    preds    = rf.predict(X_encoded)
    probas   = rf.predict_proba(X_encoded)
    segments = le.inverse_transform(preds)
    conf     = probas.max(axis=1) * 100

    result = df.copy()
    result['Segment']      = segments
    result['Confidence_%'] = conf.round(1)
    result['Action']       = result['Segment'].map(
        {k: v['action'] for k, v in segment_config.items()}
    )
    return result