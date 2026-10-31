"""
Generative AI Engine for Student Performance Intelligence System
Integrates with Google Gemini API for:
1. Student Academic Mentoring & Study Coaching (Supports Hinglish & English)
2. Teacher Pedagogical Intervention & Communication Drafting (Supports Hinglish & English)
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

def _generate_local_student_coaching_hinglish(student, prompt_topic):
    """Deep heuristic pedagogical synthesis in natural, supportive Hinglish."""
    name = student.get("Name", "Student").split()[0]
    score = student.get("Performance_Score", 0)
    att = student.get("Attendance", 0)
    study = student.get("Study_Hours", 0)
    internal = student.get("Internal_Marks", 0)
    quiz = student.get("Quiz_Average", 0)
    prac = student.get("Practical_Score", 0)
    weak_areas = student.get("Improvement_Areas", [])

    p_lower = prompt_topic.lower()

    if any(k in p_lower for k in ["schedule", "timetable", "routine", "time", "plan"]):
        primary_focus = weak_areas[0] if weak_areas else "Quiz Practice"
        return f"""### 📅 Aapka Personalized 7-Day Study Routine ({name})

Aapke current metrics (Attendance: {att:.1f}%, Daily Study: {study:.1f} hrs, Score: {score}/100) ke hisab se:

1. **Monday - Wednesday (Main Focus Block: {primary_focus}):**
   - Har din shuru ke 45 minutes apne sabse weak area **{primary_focus}** par lagayein.
   - Pehle class notes aur basic concepts revise karein, fir 5 practice questions bina dekhe solve karein.
2. **Thursday - Friday (Lab & Practical Work Continuity):**
   - Daily 1 ghanta practical lab exercises aur viva concepts ke liye nikaalein (Current Lab Score: {prac}/100).
   - Saare pending assignments aur teacher feedback ko review karke mistakes correct karein.
3. **Saturday (Active Recall & Quiz Revision):**
   - Short timed practice quizzes attempt karein (Current Quiz Avg: {quiz}/100). Regular quiz lagane se exam retention 40% tak improve hota hai.
4. **Sunday (Progress Review & Target Planning):**
   - 30 minutes nikaal kar poore hafte ki study log check karein. What-If Simulator chala kar dekhein ki attendance aur study hours badhane se aapka score kitna jump karega!"""

    if any(k in p_lower for k in ["practical", "lab", "viva"]):
        return f"""### 🔬 Practical & Laboratory Improvement Blueprint ({name})

Aapka current practical score **{prac}/100** hai. Ise 80+ distinction tier me laane ke liye ye steps follow karein:
1. **Pre-Lab Preparation:** Lab session me jaane se pehle experiment ke objective aur circuit/code ko 15 minute pehle padhein. Isse lab me debugging ka time bachega.
2. **Hands-On Verification:** Lab partner ke code ya reading par depend na rahein; saare practical experiments khud execute karein.
3. **Viva Voce Readiness:** Har practical ke sath aane wale 3-4 conceptual viva questions pehle se prepare karein. Viva marks internal score ko direct boost karte hain!"""

    if any(k in p_lower for k in ["exam", "marks", "improve", "score", "maximize"]):
        return f"""### 🎯 High-Impact Exam Maximization Strategy ({name})

Apne academic score ko **{score:.1f}** se top grade tak le jaane ke liye:
1. **Attendance Leverage ({att:.1f}%):** Internal examination marks me class attendance ka direct weightage hota hai. Aane wale month me 85%+ attendance maintain karein.
2. **Internal Exam Focus ({internal}/100):** Mid-term exam me jin specific chapters me marks kate the, pehle unhe target karein.
3. **Daily Study Habit:** Daily study time ko **{study:.1f} ghante** se badhakar **{min(6.0, study + 1.5):.1f} ghante** karein. Chhoti regular revision pre-exam stress ko 50% kam karti hai!"""

    # Default comprehensive coaching response
    focus_str = ", ".join(weak_areas) if weak_areas else "General Revision"
    return f"""### 💡 AI Academic Coaching Note ({name})

Namaste {name}! Aapka current academic profile:
- **Academic Score:** {score:.1f} / 100 ({student.get('Performance_Status', 'Stable')})
- **Risk Level:** {student.get('Risk_Level', 'Low')}
- **Priority Improvement Indicators:** {focus_str}

**Immediate Action Steps:**
1. **Daily Incremental Revision:** Abhi aapka study time {study:.1f} ghante/din hai. Roz shaam ko 90 minute ka fixed revision slot banayein.
2. **Weak Areas First:** Apne lowest metrics ({focus_str}) ko pehle cover karein. Learning Materials section se teacher ke notes download karke padhein.
3. **Self-Assessment:** Is dashboard par diya gaya Practice Quiz hafte me 2 baar solve karein taaki concepts fresh rahein!"""


def _generate_local_student_coaching_english(student, prompt_topic):
    """Deep heuristic pedagogical synthesis in standard English."""
    name = student.get("Name", "Student").split()[0]
    score = student.get("Performance_Score", 0)
    att = student.get("Attendance", 0)
    study = student.get("Study_Hours", 0)
    internal = student.get("Internal_Marks", 0)
    quiz = student.get("Quiz_Average", 0)
    prac = student.get("Practical_Score", 0)
    weak_areas = student.get("Improvement_Areas", [])

    p_lower = prompt_topic.lower()

    if any(k in p_lower for k in ["schedule", "timetable", "routine", "time", "plan"]):
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

    if any(k in p_lower for k in ["practical", "lab", "viva"]):
        return f"""### 🔬 Laboratory & Practical Improvement Guide for {name}

Your recorded practical score is **{prac}/100**. To push this into the 80+ distinction tier:
- **Pre-Lab Preparation:** Read experiment objectives before stepping into the lab session. Understanding theoretical formulas reduces debugging time.
- **Hands-On Verification:** Do not rely solely on partner outputs; write your own code / record individual measurements.
- **Viva Voce Readiness:** Prepare 3 conceptual questions related to each completed practical unit."""

    if any(k in p_lower for k in ["exam", "marks", "improve", "score", "maximize"]):
        return f"""### 🎯 High-Impact Exam Maximization Strategy for {name}

To bridge your performance score from **{score:.1f}** to the next grade tier:
1. **Attendance Leverage ({att:.1f}%):** Class continuity is the single biggest predictor of internal evaluation scores. Aim for consistent 85%+ attendance.
2. **Internal Revision Target ({internal}/100):** Focus on specific chapters where questions were missed in mid-term evaluations.
3. **Targeted Daily Habit:** Increasing daily study time from **{study:.1f} hours** to **{min(6.0, study + 1.5):.1f} hours** will significantly reduce pre-exam stress."""

    focus_str = ", ".join(weak_areas) if weak_areas else "General Revision"
    return f"""### 💡 AI Academic Coaching Note for {name}

Hello {name}! Reviewing your current performance profile:
- **Academic Score:** {score:.1f}/100 ({student.get('Performance_Status', 'Stable')})
- **Risk Level:** {student.get('Risk_Level', 'Low')}
- **Priority Improvement Indicators:** {focus_str}

**Recommended Immediate Actions:**
1. **Daily Incremental Revision:** Your logged study hours are {study:.1f} hrs/day. Building a fixed 90-minute evening revision block will deliver consistent compounding gains.
2. **Targeting Weak Links:** Prioritize your lowest metrics ({focus_str}). Download teacher-uploaded materials from your portal.
3. **Continuous Self-Assessment:** Use the interactive practice quiz on this dashboard twice weekly to track retention."""


def _generate_local_teacher_advisor_hinglish(student, action_type):
    """Deep pedagogical synthesis for educators in natural, professional Hinglish."""
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
    status = student.get('Performance_Status', 'Stable')

    if action_type == "parent_letter":
        return f"""OFFICIAL ACADEMIC ADVISORY & PARENT COMMUNICATION (HINGLISH)
Date: Current Academic Term
To: {name} (Student ID: {sid}) ke Parents / Guardians
Department: {dept}

Subject: Student Academic Progress aur Remedial Support ke Sambandh me

Aadarniya Parents / Guardians,

Department of {dept} ki taraf se hum {name} ki academic performance aur continuous assessments ki update share kar rahe hain:

Current Academic Snapshot:
• Overall Composite Score: {score:.1f} / 100
• Class Attendance: {att:.1f}% (Institutional Minimum: 75%)
• Daily Self-Study Hours: {study:.1f} ghante/din
• Current Academic Status: {status} (Risk Level: {risk})
• Main Focus Areas: {weak_str}

Faculty Recommendation:
{name} me academic potential kaafi accha hai. Aane wale semester examinations me best results laane ke liye ghar par daily 3-4 ghante ka focused study routine banana aur regular class attend karna bahut zaroori hai. Hamare faculty mentors personalized academic guidance ke liye hamesha available hain.

Dhanyawad,
Faculty Academic Mentorship Committee
Department of {dept}"""

    if action_type == "remedial_plan":
        return f"""PEDAGOGICAL INTERVENTION & REMEDIAL ROADMAP (HINGLISH)
Student: {name} ({sid}) | Department: {dept}
Risk Level: {risk} (Risk Score: {risk_score}/14) | Mukhya Zaroorat: {insight}

Phase 1: Academic Diagnostic & Concept Alignment (Week 1)
• Student ke sath 15-minute ki 1-on-1 counseling session conduct karein.
• Weak indicators ({weak_str}) me student ki understanding check karein.
• Portal par uploaded learning materials aur question banks access karwayein.

Phase 2: Targeted Practice & Peer Mentorship (Weeks 2 - 3)
• Har lagging topic par micro-assignments assign karein.
• Class ke top peer mentor ke sath study buddy pair banayein.
• Attendance monitor karein aur 80%+ regular attendance ensure karein.

Phase 3: Formative Re-Evaluation & Follow-up (Week 4)
• Short practice test conduct karein taaki improvement measure ho sake.
• Risk indicators dobara evaluate karke institutional log me update karein."""

    return f"""FACULTY OBSERVATION & MENTORING MEMORANDUM (HINGLISH)
Student: {name} ({sid}) | Department: {dept}
Evaluation Snapshot: Score {score:.1f}/100 | Risk: {risk} | Insight: {insight}

Mukhya Observations:
1. Academic Performance: Student ka attendance record {att:.1f}% hai aur internal marks {student.get('Internal_Marks', 0)}/100 hain.
2. Vulnerability Area: Sabse bada gap [{weak_str}] me dekha gaya hai.
3. Teacher Action: Lab sessions me concept clarity par personal feedback dein aur regular assignments verify karein."""


def _generate_local_teacher_advisor_english(student, action_type):
    """Deep pedagogical synthesis for educators in standard formal English."""
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

Phase 2: Structured Remedial Work & Targeted Practice (Weeks 2 - 3)
• Assign targeted micro-exercises covering lagging modules.
• Pair with an academic peer mentor or student study group.

Phase 3: Formative Re-Evaluation & Follow-up (Week 4)
• Administer a diagnostic practice quiz to measure retention.
• Re-evaluate composite risk score and record notes in the tracking dashboard."""

    return f"""FACULTY OBSERVATION & MENTORING MEMORANDUM
Student: {name} ({sid}) | Department: {dept}
Evaluation Snapshot: Score {score:.1f}/100 | Risk: {risk} | Insight: {insight}

Key Pedagogical Observations:
1. Academic Metrics: Student holds an attendance record of {att:.1f}% and internal mark of {student.get('Internal_Marks', 0)}/100.
2. Primary Vulnerability: Main performance gap flagged in [{weak_str}].
3. Recommended Teacher Action: Focus personal feedback during lab sessions on concept clarity."""


# =========================================================================
# PUBLIC INTERFACE
# =========================================================================

def ask_student_mentor(student_dict, question, api_key=None, lang="hinglish"):
    """
    Handles student mentoring queries in Hinglish (default) or English.
    Uses Gemini API if key is available; falls back to Smart Local Engine seamlessly.
    """
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY")
    is_hinglish = (lang or "").lower() == "hinglish"

    if key_to_use:
        name = student_dict.get("Name", "Student")
        lang_instruction = (
            "IMPORTANT: Respond in natural, encouraging, friendly Hinglish (Hindi written in clean English/Roman script), "
            "the way an approachable Indian professor or college mentor guides students. Keep technical terms in English "
            "(e.g. 'Attendance', 'Practical', 'Quiz', 'Assignment', 'Revision') but explain everything in conversational Hinglish."
            if is_hinglish else
            "Respond in encouraging, formal, concise English."
        )
        system_instruction = (
            f"You are an empathetic, world-class university academic coach mentoring {name}. "
            f"Student metrics: Score={student_dict.get('Performance_Score')}/100, "
            f"Attendance={student_dict.get('Attendance')}%, Study Hours={student_dict.get('Study_Hours')}h/day, "
            f"Internal={student_dict.get('Internal_Marks')}, Quiz={student_dict.get('Quiz_Average')}, "
            f"Practical={student_dict.get('Practical_Score')}, Department={student_dict.get('Department')}. "
            f"{lang_instruction} Format response cleanly using markdown with bold headings and bullet points."
        )
        gemini_text, status = _call_gemini_api(question, key_to_use, system_instruction)
        if gemini_text:
            return {
                "answer": gemini_text,
                "engine": f"Google Gemini 1.5 Flash ({'Hinglish' if is_hinglish else 'English'})",
                "status": "online",
                "lang": "hinglish" if is_hinglish else "english"
            }

    # Seamless Fallback
    local_text = _generate_local_student_coaching_hinglish(student_dict, question) if is_hinglish else _generate_local_student_coaching_english(student_dict, question)
    return {
        "answer": local_text,
        "engine": f"SPI Intelligent Pedagogical Engine ({'Hinglish' if is_hinglish else 'English'})",
        "status": "offline_fallback",
        "lang": "hinglish" if is_hinglish else "english"
    }


def ask_teacher_advisor(student_dict, action_type, custom_prompt="", api_key=None, lang="hinglish"):
    """
    Handles teacher pedagogical action generation in Hinglish (default) or English.
    action_type: 'parent_letter', 'remedial_plan', 'observation_note', or 'custom'
    """
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY")
    is_hinglish = (lang or "").lower() == "hinglish"

    if key_to_use:
        lang_instruction = (
            "IMPORTANT: Draft the document in professional, natural Hinglish (Hindi written in Roman/English script) "
            "suitable for Indian academic institutions and parents, keeping key academic terms in English."
            if is_hinglish else
            "Draft the document in formal, professional higher-education English."
        )
        system_instruction = (
            "You are an expert higher-education pedagogical consultant and academic mentor. "
            f"{lang_instruction} "
            "Draft high-impact documents such as parent advisories, remedial roadmaps, and observation notes."
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
                "engine": f"Google Gemini 1.5 Flash ({'Hinglish' if is_hinglish else 'English'})",
                "status": "online",
                "lang": "hinglish" if is_hinglish else "english"
            }

    # Seamless Fallback
    local_text = _generate_local_teacher_advisor_hinglish(student_dict, action_type) if is_hinglish else _generate_local_teacher_advisor_english(student_dict, action_type)
    return {
        "content": local_text,
        "engine": f"SPI Intelligent Pedagogical Engine ({'Hinglish' if is_hinglish else 'English'})",
        "status": "offline_fallback",
        "lang": "hinglish" if is_hinglish else "english"
    }
