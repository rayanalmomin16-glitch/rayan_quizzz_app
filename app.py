import streamlit as st
import json
import os
import random  # دمج مميزات العشوائية للأسئلة في لغة بايثون

# 1. إعدادات الصفحة وعنوان التطبيق في المتصفح
st.set_page_config(page_title="تطبيق ريان الذكي VIP", page_icon="🏎️", layout="centered")

# دالة لقراءة الأسئلة من ملف الـ JSON ومحمية من الـ Cache لضمان التحديث المستمر
def load_huge_quiz_bank():
    file_path = "quiz_data.json"
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {
                "⚠️ خطأ في الملف": [{"q": "ملف quiz_data.json يحتوي على خطأ في بنية الـ JSON، يرجى إصلاحه.", "options": ["مفهوم", "تحديث"], "correct": 0}]
            }
    else:
        return {
            "🚨 الملف مفقود": [{"q": "ملف quiz_data.json غير موجود أو فارغ! يرجى رفعه في نفس المجلد.", "options": ["حسناً", "سأرفعه"], "correct": 0}]
        }

quiz_bank = load_huge_quiz_bank()

# إعداد الـ CSS المخصص للخلفية والتحسينات البصرية
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #ff9a9e, #fecfef, #a1c4fd, #c2e9fb);
        background-size: 400% 400%;
        animation: gradientAnimation 12s ease infinite;
    }
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-title { 
        font-size: 45px !important; font-weight: 900; text-align: center; color: #2c3e50; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px;
    }
    .sub-title { 
        font-size: 22px; text-align: center; color: #34495e; margin-bottom: 30px; font-weight: bold;
    }
    .question-box {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 15px;
        border-right: 5px solid #ff4b4b;
        transition: transform 0.3s ease;
    }
    .question-box:hover { transform: translateY(-3px); }
    
    div.stButton > button {
        background: linear-gradient(90deg, #ff4b4b, #ff7676) !important;
        color: white !important; border: none !important; border-radius: 25px !important;
        padding: 10px 24px !important; font-weight: bold !important; font-size: 18px !important;
        box-shadow: 0 4px 10px rgba(255, 75, 75, 0.3) !important; transition: all 0.3s ease !important;
    }
    div.stButton > button:hover { transform: scale(1.02) !important; }
    
    div[data-testid="stRadio"] div[role="radiogroup"] {
        background-color: rgba(255, 255, 255, 0.7); padding: 15px; border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">👑 منظومة ريان المعرفية VIP</div>', unsafe_allow_html=True)

# إدارة الصفحات عبر الـ Session State
if 'page' not in st.session_state:
    st.session_state.page = "main_menu"
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'sampled_questions' not in st.session_state:
    st.session_state.sampled_questions = []

if st.session_state.selected_category and st.session_state.selected_category not in quiz_bank:
    st.session_state.page = "main_menu"
    st.session_state.selected_category = None

# --- الصفحة الرئيسية: اختيار القسم ---
if st.session_state.page == "main_menu":
    st.markdown('<div class="sub-title">اختر قسماً لتبدأ التحدي والمنافسة في المعلومات فوراً:</div>', unsafe_allow_html=True)
    
    chosen_cat = st.radio("🎯 اختر القسم المناسب لتحديك:", options=list(quiz_bank.keys()), index=0)
    st.markdown("---")
    
    if st.button("🚀 ارفع التحدي وابدأ الاختبار الآن", use_container_width=True):
        st.session_state.selected_category = chosen_cat
        all_questions = quiz_bank[chosen_cat]
        num_to_sample = min(5, len(all_questions))
        st.session_state.sampled_questions = random.sample(all_questions, num_to_sample)
        st.session_state.user_answers = [None] * num_to_sample
        st.session_state.page = "quiz_page"
        st.rerun()

# --- صفحة الأسئلة والاختبار ---
elif st.session_state.page == "quiz_page":
    category = st.session_state.selected_category
    questions = st.session_state.sampled_questions
    total_q = len(questions)
    
    st.markdown(f'<div class="sub-title">أنت الآن داخل تحدي قسم: <b>{category}</b></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    for idx, item in enumerate(questions):
        st.markdown(f'<div class="question-box"><h3>السؤال {idx + 1}: {item["q"]}</h3></div>', unsafe_allow_html=True)
        
        current_index = None
        if st.session_state.user_answers[idx] in item['options']:
            current_index = item['options'].index(st.session_state.user_answers[idx])
            
        choice = st.radio(
            label=f"question_label_{idx}",
            options=item['options'],
            key=f"quiz_{category}_{idx}",
            index=current_index,
            label_visibility="collapsed"
        )
        st.session_state.user_answers[idx] = choice
        st.markdown("---")
        
    col_submit, col_back = st.columns(2)
    
    if col_submit.button("📝 الحساب وتقديم الإجابات", use_container_width=True):
        if None in st.session_state.user_answers:
            st.warning("⚠️ يرجى الإجابة على جميع الأسئلة أولاً قبل تقديم الاختبار!")
        else:
            correct_count = 0
            wrong_questions = []
            
            for idx, item in enumerate(questions):
                user_choice = st.session_state.user_answers[idx]
                correct_choice = item['options'][item['correct']]
                
                if user_choice == correct_choice:
                    correct_count += 1
                else:
                    wrong_questions.append({
                        "num": idx + 1, "q": item['q'], "user_ans": user_choice, "correct_ans": correct_choice
                    })
                    
            percentage = (correct_count / total_q) * 100
            st.balloons()
            st.success("### 🎉 تم اكتمال الاختبار بنجاح!")
            
            # تم تعديل هذا الجزء لحل مشكلة col1 التي تسببت في الخطأ
            st.metric(label="الأسئلة الصحيحة", value=f"{correct_count} / {total_q}")
            st.metric(label="نسبة نجاحك", value=f"{percentage:.1f}%")
            st.progress(correct_count / total_q)
            
            if percentage == 100:
                st.snow()
                st.write("### 🌟 أسطورة حقيقية! إجاباتك مثالية عبقري لا يخطئ!")
            elif percentage >= 80:
                st.write("### 👍 رائع جداً! معلوماتك قوية وفي تقدم مستمر.")
            elif percentage >= 50:
                st.write("### 😉 نتيجة جيدة! لكن تحتاج إلى بعض التركيز.")
            else:
                st.write("### 👎 لا بأس، حاول مجدداً لتطوير قدراتك!")
                
            st.markdown("---")
            
            if wrong_questions:
                st.error("### ❌ مراجعة وتصحيح الأخطاء:")
                for w in wrong_questions:
                    with st.expander(f"🔍 السؤال {w['num']}: {w['q']}"):
                        st.markdown(f"**إجابتك:** <span style='color:red; font-weight:bold;'>{w['user_ans']}</span>", unsafe_allow_html=True)
                        st.markdown(f"**الإجابة الصحيحة:** <span style='color:gree; font-weight:bold;'>{w['correct_ans']}</span>", unsafe_allow_html=True)
            else:
                st.success("### 🏆 مبروك! إجاباتك كلها صحيحة 100%.")

    if col_back.button("↩️ العودة للقائمة الرئيسية", use_container_width=True):
        st.session_state.page = "main_menu"
        st.session_state.selected_category = None
        st.session_state.sampled_questions = []
        st.rerun()
