import streamlit as st
import pandas as pd
import joblib

# Load the trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("Phishing Email Classifier")

def classify_email(email_text):
    email_vector = vectorizer.transform([email_text])
    prediction = model.predict(email_vector)[0]
    probability = model.predict_proba(email_vector)[0]
    result = "PHISHING" if prediction == 1 else "LEGITIMATE"
    confidence = max(probability) * 100
    return result, confidence

# --- Single email classifier ---
email_text = st.text_area("Paste email text here:")
if st.button("Classify"):
    if email_text.strip() == "":
        st.warning("Please paste some email text first.")
    else:
        result, confidence = classify_email(email_text)
        st.write(f"**Result:** {result} ({confidence:.1f}% confidence)")

st.divider()

# --- Batch analysis via CSV upload ---
st.subheader("Batch Analysis: Upload a CSV")
st.caption("CSV should have a column named 'email_text'")

uploaded_file = st.file_uploader("Upload a CSV of emails", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of your data:")
    st.dataframe(df)

    st.write("DEBUG: Reached the email_text check")
    if "email_text" in df.columns:
        st.write("DEBUG: email_text column found, starting classification")
        try:
            results = df["email_text"].apply(classify_email)
            df["prediction"] = results.apply(lambda x: x[0])
            df["confidence"] = results.apply(lambda x: round(x[1], 1))

            st.write("Classified Results:")
            st.dataframe(df)

            st.write("Basic Stats:")
            st.write(f"Total emails: {len(df)}")
            st.write(f"Phishing detected: {(df['prediction'] == 'PHISHING').sum()}")
            st.write(f"Legitimate: {(df['prediction'] == 'LEGITIMATE').sum()}")
            st.write(f"Average confidence: {df['confidence'].mean():.1f}%")
            st.write(f"Max confidence: {df['confidence'].max():.1f}%")
        except Exception as e:
            st.error(f"Something broke during classification: {e}")
    else:
        st.error("CSV must have a column named 'email_text'")
