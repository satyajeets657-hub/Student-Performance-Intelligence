"""
Machine Learning Engine for Student Performance Intelligence System
Trains and evaluates:
1. Random Forest Regressor for Final Marks Prediction
2. Random Forest Classifier for At-Risk Academic Support Classification
Provides Feature Importances and SHAP-like explanations.
"""

import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, classification_report
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "students.csv"
MODEL_DIR = BASE_DIR / "models"

FEATURE_COLS = [
    "Attendance",
    "Study_Hours",
    "Assignment_Submission_Rate",
    "Assignment_Score",
    "Quiz_Average",
    "Practical_Score",
    "Internal_Marks",
    "Previous_Semester_Score",
]

FEATURE_LABELS = {
    "Attendance": "Class Attendance",
    "Study_Hours": "Daily Study Hours",
    "Assignment_Submission_Rate": "Submission Regularity",
    "Assignment_Score": "Assignment Quality",
    "Quiz_Average": "Quiz Performance",
    "Practical_Score": "Lab / Practical Work",
    "Internal_Marks": "Internal Examination",
    "Previous_Semester_Score": "Past Academic Record",
}


def _compute_risk_and_support(df):
    """Compute deterministic ground-truth risk and support labels for training."""
    def r_score(row):
        score = 0
        if row['Attendance'] < 60: score += 3
        elif row['Attendance'] < 75: score += 2
        elif row['Attendance'] < 85: score += 1
        if row['Study_Hours'] < 2: score += 3
        elif row['Study_Hours'] < 4: score += 1
        if row['Final_Marks'] < 50: score += 3
        elif row['Final_Marks'] < 65: score += 2
        elif row['Final_Marks'] < 75: score += 1
        if row['Practical_Score'] < 50: score += 2
        elif row['Practical_Score'] < 60: score += 1
        if row['Assignment_Score'] < 50: score += 2
        if row['Quiz_Average'] < 50: score += 2
        return score

    risk_scores = df.apply(r_score, axis=1)
    support_flags = risk_scores.apply(
        lambda s: "High Priority" if s >= 6 else ("Needs Support" if s >= 3 else "Normal")
    )
    return support_flags


def train_models():
    """Trains regression and classification models, saves artifacts and metrics."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH).drop_duplicates()

    df["Support_Flag"] = _compute_risk_and_support(df)

    X = df[FEATURE_COLS]
    y_reg = df["Final_Marks"]
    y_clf = df["Support_Flag"]

    # Split
    X_train, X_test, y_reg_train, y_reg_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )
    _, _, y_clf_train, y_clf_test = train_test_split(
        X, y_clf, test_size=0.2, random_state=42
    )

    # 1. Regressor: Random Forest
    reg_model = RandomForestRegressor(n_estimators=120, max_depth=8, random_state=42)
    reg_model.fit(X_train, y_reg_train)
    y_reg_pred = reg_model.predict(X_test)

    r2 = round(r2_score(y_reg_test, y_reg_pred), 3)
    mae = round(mean_absolute_error(y_reg_test, y_reg_pred), 2)

    # 2. Classifier: Random Forest
    clf_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf_model.fit(X_train, y_clf_train)
    y_clf_pred = clf_model.predict(X_test)

    acc = round(accuracy_score(y_clf_test, y_clf_pred) * 100, 1)

    # Feature Importance (percentage)
    importances = reg_model.feature_importances_
    total_imp = sum(importances)
    feat_importance_dict = {
        FEATURE_LABELS[col]: round(float(imp / total_imp) * 100, 1)
        for col, imp in zip(FEATURE_COLS, importances)
    }
    # Sort descending
    sorted_importances = dict(sorted(feat_importance_dict.items(), key=lambda item: item[1], reverse=True))

    artifacts = {
        "reg_model": reg_model,
        "clf_model": clf_model,
        "classes": list(clf_model.classes_),
        "metrics": {
            "r2_score": r2,
            "mae": mae,
            "accuracy": acc,
            "total_samples": len(df),
            "test_samples": len(X_test),
        },
        "feature_importances": sorted_importances,
        "features": FEATURE_COLS,
    }

    joblib.dump(artifacts, MODEL_DIR / "student_ml_bundle.joblib")
    return artifacts


_LOADED_BUNDLE = None


def get_ml_bundle():
    """Lazy load or train on first call."""
    global _LOADED_BUNDLE
    if _LOADED_BUNDLE is not None:
        return _LOADED_BUNDLE

    bundle_path = MODEL_DIR / "student_ml_bundle.joblib"
    if bundle_path.exists():
        try:
            _LOADED_BUNDLE = joblib.load(bundle_path)
            return _LOADED_BUNDLE
        except Exception:
            pass

    _LOADED_BUNDLE = train_models()
    return _LOADED_BUNDLE


def predict_student_performance(student_dict):
    """
    Given a student dictionary or features dict, returns:
    - Predicted Final Marks (float)
    - Predicted Risk Level & Support Flag
    - Class Probabilities
    - Top Contributing Factors
    """
    bundle = get_ml_bundle()
    reg = bundle["reg_model"]
    clf = bundle["clf_model"]

    row_vals = []
    for f in FEATURE_COLS:
        val = student_dict.get(f, 0.0)
        try:
            row_vals.append(float(val))
        except (ValueError, TypeError):
            row_vals.append(0.0)

    X_sample = pd.DataFrame([row_vals], columns=FEATURE_COLS)

    pred_marks = round(float(reg.predict(X_sample)[0]), 1)
    pred_support = str(clf.predict(X_sample)[0])

    probs = clf.predict_proba(X_sample)[0]
    class_probs = {
        cls: round(float(prob) * 100, 1)
        for cls, prob in zip(clf.classes_, probs)
    }

    # Factor Analysis: How this student compares to feature baseline
    strengths = []
    risk_drivers = []
    if float(student_dict.get("Attendance", 0)) < 75:
        risk_drivers.append("Low Attendance (<75%)")
    else:
        strengths.append("High Attendance")

    if float(student_dict.get("Study_Hours", 0)) < 3.0:
        risk_drivers.append("Limited Daily Study Hours (<3h)")
    else:
        strengths.append("Consistent Study Habit")

    if float(student_dict.get("Practical_Score", 0)) < 65:
        risk_drivers.append("Practical Lab Score Lagging")
    if float(student_dict.get("Quiz_Average", 0)) < 65:
        risk_drivers.append("Quiz Revision Required")

    return {
        "predicted_final_marks": pred_marks,
        "predicted_support_flag": pred_support,
        "probabilities": class_probs,
        "metrics": bundle["metrics"],
        "feature_importances": bundle["feature_importances"],
        "risk_drivers": risk_drivers,
        "strengths": strengths,
    }


if __name__ == "__main__":
    print("Training ML Models...")
    res = train_models()
    print("Training Complete!")
    print(f"R2 Score: {res['metrics']['r2_score']}")
    print(f"MAE: {res['metrics']['mae']}")
    print(f"Risk Classifier Accuracy: {res['metrics']['accuracy']}%")
    print("Feature Importances:", res["feature_importances"])
