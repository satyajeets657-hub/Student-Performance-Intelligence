"""
Generative AI Engine for Student Performance Intelligence System
Integrates with Google Gemini API for:
1. Student Academic Mentoring & Study Coaching
2. Teacher Pedagogical Intervention & Communication Drafting
Includes Intelligent Local Fallback Engine (Zero-Downtime offline mode).
"""

import os
import json
import urllib.request
import urllib.error

# Default Gemini Model
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")


def _call_gemini_api(prompt, api_key, system_instruction=None):
    """Calls Google Gemini REST API directly with timeout and error handling."""
    if not api_key:
        return None, "No API key provided"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"

    contents = []
    if system_instruction:
        contents.append({
            "role": "user",
            "parts": [{"text": f"SYSTEM INSTRUCTION: {system_instruction}\n\nUSER PROMPT: {prompt}"}]
        })
    else:
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            result = json.loads(response.read().decode("utf-8"))
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip(), "success"
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return None, f"Gemini API Error ({e.code}): {err_msg}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

    return None, "No output candidate returned from Gemini"


# =========================================================================
# SMART LOCAL PEDAGOGICAL GENERATOR (Zero-Downtime Offline Fallback)
# =========================================================================

def _generate_local_student_coaching(student, prompt_topic):
    """Deep heuristic pedagogical synthesis for student coaching."""
    name = student.get("Name", "Student").split()[0]
    score = student.get("Performance_Score", 0)
    att = student.get("Attendance", 0)
    study = student.get("Study_Hours", 0)
    internal = student.get("Internal_Marks", 0)
    quiz = student.get("Quiz_Average", 0)
    prac = student.get("Practical_Score", 0)
    weak_areas = student.get("Improvement_Areas", [])

    p_lower = prompt_topic.lower()

    if "schedule" in p_lower or "timetable" in p_lower or "routine" in p_lower:
        primary_focus = weak_areas[0] if weak_areas else "Quiz Practice"
        return f"""### 📅 Personalized 7-Day Academic Routine for {name}

Based on your current metrics (Attendance: {att:.1f}%, Daily Study: {study:.1f} hrs, Score: {score}/100):

1. **Monday - Wednesday (Focus Block: {primary_focus}):**
   - Spend the first 45 minutes targeting your identified gap: **{primary_focus}**.
   - Review fundamental notes and attempt 5 practice problems before touching familiar topics.
2. **Thursday - Friday (Assessment & Lab Continuity):**
   - Dedicate 1 hour to Practical exercises and internal assessment review (current lab score: {prac}/100).
   - Verify all pending coursework and assignment feedback.
3. **Saturday (Active Recall & Quiz Revision):**
   - Take short timed self-quizzes (current quiz avg: {quiz}/100). Active retrieval increases exam retention by 40%.
4. **Sunday (Reflection & Weekly Review):**
   - Spend 30 minutes evaluating your weekly study log. Re-run the What-If Simulator to check progress toward your target score!"""

    if "practical" in p_lower or "lab" in p_lower:
        return f"""### 🔬 Laboratory & Practical Improvement Guide for {name}

Your recorded practical score is **{prac}/100**. To push this into the 80+ distinction tier:
- **Pre-Lab Preparation:** Read experiment objectives before stepping into the lab session. Understanding the theoretical formulas reduces debugging time.
- **Hands-On Verification:** Do not rely solely on partner outputs; write your own code / record individual measurements.
- **Viva Voce Readiness:** Prepare 3 conceptual questions related to each completed practical unit. Demonstrating conceptual depth in viva tests accounts for significant internal marks."""

    if "exam" in p_lower or "marks" in p_lower or "improve" in p_lower:
        return f"""### 🎯 High-Impact Exam Maximization Strategy for {name}

To bridge your performance score from **{score:.1f}** to the next grade tier:
1. **Attendance Leverage ({att:.1f}%):** Class continuity is the single biggest predictor of internal evaluation scores. Aim for consistent 85%+ attendance over the next month.
2. **Internal Revision Target ({internal}/100):** Focus on the specific chapters where questions were missed in the mid-term evaluations.
3. **Targeted Daily Habit:** Increasing daily focused study time from **{study:.1f} hours** to **{min(6.0, study + 1.5):.1f} hours** will significantly reduce pre-exam stress and increase retention."""

    # Default comprehensive coaching response
    focus_str = ", ".join(weak_areas) if weak_areas else "General Revision"
    return f"""### 💡 AI Academic Coaching Note for {name}

Hello {name}! Reviewing your current performance profile:
- **Academic Score:** {score:.1f}/100 ({student.get('Performance_Status', 'Stable')})
- **Risk Level:** {student.get('Risk_Level', 'Low')}
- **Priority Improvement Indicators:** {focus_str}

**Recommended Immediate Actions:**
1. **Daily Incremental Revision:** Your logged study hours are {study:.1f} hrs/day. Building a fixed 90-minute evening revision block will deliver consistent compounding gains.
2. **Targeting Weak Links:** Prioritize your lowest metrics ({focus_str}). Download the teacher-uploaded learning materials from your portal for structured revision.
3. **Continuous Self-Assessment:** Use the interactive practice quiz on this dashboard twice weekly to track concept retention."""


def _generate_local_teacher_advisor(student, action_type):
    """Deep pedagogical synthesis for educator intervention and communication."""
    name = student.get("Name", "Student")
    sid = student.get("Student_ID", "N/A")
    dept = student.get("Department", "Academic Department")
    score = student.get("Performance_Score", 0)
    att = student.get("Attendance", 0)
    study = student.get("Study_Hours", 0)
    risk = student.get("Risk_Level", "Low")
    risk_score = student.get("Risk_Score", 0)
    insight = student.get("Primary_Insight", "Stable")
    weak_areas = student.get("Improvement_Areas", [])
    weak_str = ", ".join(weak_areas) if weak_areas else "None"

    if action_type == "parent_letter":
        return f"""OFFICIAL ACADEMIC ADVISORY & PARENT COMMUNICATION
Date: Current Academic Term
To: Parents / Guardians of {name} (Student ID: {sid})
Department: {dept}

Subject: Academic Progress Advisory and Support Plan

Dear Parent/Guardian,

We are writing from the Department of {dept} to provide an update regarding {name}'s academic trajectory and to request your active partnership in supporting their academic success.

Current Academic Overview:
• Composite Academic Score: {score:.1f} / 100
• Class Attendance Record: {att:.1f}% (Institutional Minimum: 75%)
• Average Daily Study Hours: {study:.1f} hrs/day
• Current Academic Standing: {student.get('Performance_Status', 'Stable')} (Risk Category: {risk})
• Primary Focus Areas: {weak_str}

Observation & Recommended Collaboration:
Our continuous assessment system indicates that while {name} demonstrates clear potential, proactive support in {"maintaining regular class attendance" if att < 75 else "consistent daily study routines"} and completing continuous assignments is essential before upcoming semester examinations.

We recommend establishing a structured home study schedule of at least 3-4 hours daily and encouraging regular class participation. Our faculty mentor team is available for one-on-one academic consultation.

Sincerely,
Faculty Academic Mentorship Committee
Department of {dept}"""

    if action_type == "remedial_plan":
        return f"""PEDAGOGICAL INTERVENTION & REMEDIAL ROADMAP
Target Student: {name} ({sid}) | Department: {dept}
Assessed Risk Level: {risk} (Score: {risk_score}/14) | Key Need: {insight}

Phase 1: Academic Diagnostic & Root-Cause Alignment (Week 1)
• Conduct a 15-minute diagnostic conference with the student.
• Review submitted coursework in key low-scoring indicators ({weak_str}).
• Ensure student access to uploaded study materials and syllabus resources.

Phase 2: Structured Remedial Work & Targeted Practice (Weeks 2 - 3)
• Assign targeted micro-exercises covering lagging modules.
• Pair with an academic peer mentor or student study group.
• Monitor class attendance and enforce a minimum 80% threshold for the upcoming period.

Phase 3: Formative Re-Evaluation & Follow-up (Week 4)
• Administer a diagnostic practice quiz to measure retention.
• Re-evaluate composite risk score and record notes in the institutional tracking dashboard."""

    # Default Educator Observation Memo
    return f"""FACULTY OBSERVATION & MENTORING MEMORANDUM
Student: {name} ({sid}) | Department: {dept}
Evaluation Snapshot: Score {score:.1f}/100 | Risk: {risk} | Insight: {insight}

Key Pedagogical Observations:
1. Academic Metrics: Student holds an attendance record of {att:.1f}% and an internal mark of {student.get('Internal_Marks', 0)}/100.
2. Primary Vulnerability: Main performance gap flagged in [{weak_str}].
3. Recommended Teacher Action: Focus personal feedback during lab sessions on concept clarity, and check submission regularity to avert semester-end academic deficits."""


# =========================================================================
# PUBLIC INTERFACE
# =========================================================================

def ask_student_mentor(student_dict, question, api_key=None):
    """
    Handles student mentoring queries.
    Uses Gemini API if key is available; falls back to Smart Local Engine seamlessly.
    """
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY")

    if key_to_use:
        name = student_dict.get("Name", "Student")
        system_instruction = (
            f"You are an empathetic, world-class university academic coach mentoring {name}. "
            f"Student metrics: Score={student_dict.get('Performance_Score')}/100, "
            f"Attendance={student_dict.get('Attendance')}%, Study Hours={student_dict.get('Study_Hours')}h/day, "
            f"Internal={student_dict.get('Internal_Marks')}, Quiz={student_dict.get('Quiz_Average')}, "
            f"Practical={student_dict.get('Practical_Score')}, Department={student_dict.get('Department')}. "
            "Give actionable, encouraging, highly specific academic advice formatted with markdown."
        )
        gemini_text, status = _call_gemini_api(question, key_to_use, system_instruction)
        if gemini_text:
            return {
                "answer": gemini_text,
                "engine": "Google Gemini 1.5 Flash (Generative AI)",
                "status": "online"
            }

    # Seamless Fallback
    local_text = _generate_local_student_coaching(student_dict, question)
    return {
        "answer": local_text,
        "engine": "SPI Intelligent Pedagogical Engine (Local AI)",
        "status": "offline_fallback"
    }


def ask_teacher_advisor(student_dict, action_type, custom_prompt="", api_key=None):
    """
    Handles teacher pedagogical action generation.
    action_type: 'parent_letter', 'remedial_plan', 'observation_note', or 'custom'
    """
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY")

    if key_to_use:
        system_instruction = (
            "You are an expert higher-education pedagogical consultant and academic mentor. "
            "Your role is to draft high-impact, professional academic documents for faculty members, "
            "such as parent communication advisories, remedial curriculum intervention plans, "
            "and student case notes using formal, empathetic institutional language."
        )
        prompt = (
            f"Generate a {action_type.replace('_', ' ')} for student {student_dict.get('Name')} "
            f"({student_dict.get('Student_ID')}, Department of {student_dict.get('Department')}). "
            f"Student metrics: Performance Score={student_dict.get('Performance_Score')}/100, "
            f"Attendance={student_dict.get('Attendance')}%, Study Hours={student_dict.get('Study_Hours')}/day, "
            f"Risk Level={student_dict.get('Risk_Level')}, Primary Insight={student_dict.get('Primary_Insight')}. "
            f"Additional teacher request: {custom_prompt or 'Standard institutional draft'}"
        )
        gemini_text, status = _call_gemini_api(prompt, key_to_use, system_instruction)
        if gemini_text:
            return {
                "content": gemini_text,
                "engine": "Google Gemini 1.5 Flash (Generative AI)",
                "status": "online"
            }

    # Seamless Fallback
    local_text = _generate_local_teacher_advisor(student_dict, action_type)
    return {
        "content": local_text,
        "engine": "SPI Intelligent Pedagogical Engine (Local AI)",
        "status": "offline_fallback"
    }
