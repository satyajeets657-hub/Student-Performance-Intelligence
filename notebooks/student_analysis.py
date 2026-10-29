import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
df = pd.read_csv(BASE / "data" / "students.csv").drop_duplicates()

# Rule-based composite performance score formulation
study_score = (df["Study_Hours"] / 6 * 100).clip(upper=100)
df["Performance_Score"] = (
    df["Final_Marks"]*.35 + df["Attendance"]*.15 + study_score*.10 +
    df["Assignment_Score"]*.10 + df["Quiz_Average"]*.10 +
    df["Practical_Score"]*.10 + df["Internal_Marks"]*.10
).round(1)

def status(x):
    if x >= 85: return "Excellent"
    if x >= 70: return "Good"
    if x >= 55: return "Stable"
    if x >= 40: return "Attention"
    return "High Risk"

df["Performance_Status"] = df["Performance_Score"].apply(status)

def risk_score(row):
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

def support(r):
    s = risk_score(r)
    return "High Priority" if s >= 6 else ("Needs Support" if s >= 3 else "Normal")

df["Support_Flag"] = df.apply(support, axis=1)
dept_avg = df.groupby("Department")["Performance_Score"].mean()
df["Department_Average"] = df["Department"].map(dept_avg).round(1)
df["Performance_Gap"] = (df["Performance_Score"]-df["Department_Average"]).round(1)

def insight(r):
    if r.Attendance < 70: return "Improve attendance"
    if r.Study_Hours < 2: return "Increase study hours"
    if r.Assignment_Submission_Rate < 70: return "Submit assignments regularly"
    if r.Quiz_Average < 55: return "Focus on quizzes"
    if r.Practical_Score < 55: return "Improve practical performance"
    if r.Performance_Gap >= 5: return "Above department average"
    return "Performance is stable"

df["Primary_Insight"] = df.apply(insight, axis=1)

print("Total students:", len(df))
print("Average performance:", round(df.Performance_Score.mean(),2))
print("Average attendance:", round(df.Attendance.mean(),2), "%")
print("Pass rate:", round((df.Grade!="F").mean()*100,2), "%")
print("\nPerformance status:\n", df.Performance_Status.value_counts())
print("\nSupport status:\n", df.Support_Flag.value_counts())

out = BASE / "outputs"
out.mkdir(parents=True, exist_ok=True)
df.to_csv(out / "student_performance_analysis_final.csv", index=False)
df[df.Support_Flag != "Normal"].sort_values("Performance_Score").to_csv(out / "students_needing_support.csv", index=False)
print("\nAnalysis complete. See outputs/.")
