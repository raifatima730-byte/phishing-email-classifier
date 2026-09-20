# Phishing Email Classifier

A machine learning model that classifies emails as phishing or legitimate using natural language processing.

## Live Demo
Try it here: https://phishing-email-classifier-e3fk2wqnvtrjcywhbakpyi.streamlit.app/

## Deployment Notes
Deployed as a live Streamlit app supporting both single-email classification and CSV batch analysis. During deployment I hit a scikit-learn version mismatch between the training environment (Colab) and production (Streamlit Cloud), which caused batch processing to fail silently. I isolated the failure point using debug logging, traced it to an indentation bug in the batch section, fixed it, and pinned matching library versions across both environments.

## What it does
Takes raw email text as input and predicts whether it's a phishing attempt or a legitimate message, with a confidence score.

## Tech Stack
- Python
- scikit-learn (TF-IDF Vectorizer + Multinomial Naive Bayes)
- Google Colab

## How it works
1. Email text is converted into numerical features using TF-IDF vectorization
2. A Naive Bayes classifier is trained on labeled phishing/legitimate examples
3. New emails are classified in real-time with a confidence percentage

## Key finding: Adversarial testing
After achieving 100% accuracy on the initial test set, I deliberately stress-tested the model with an email containing vocabulary outside the training data (a regional scam pattern using different terminology). The model failed to classify it correctly.

**Root cause:** The failure was due to limited training vocabulary, not a flaw in the algorithm itself.

**Fix:** Added targeted training examples containing the missing vocabulary and retrained the model. The same email was then correctly classified as phishing.

This demonstrates a realistic ML development cycle: build → test → find failure → diagnose → improve.

## Limitations
- Small training dataset (proof of concept, not production-scale)
- Would require much larger, more diverse data for real-world deployment
- No handling of images, attachments, or email headers — text content only

## Author
Rai — career transition into AI/security tooling

