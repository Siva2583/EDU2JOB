from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
import jwt
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json

from .models import UserPredictionHistory, PredHistory
from .utils import preprocess_input

# Add these imports at the top of your views.py
import os
import joblib
import pandas as pd
import numpy as np
from django.conf import settings

# --- Load your models using a reliable, absolute path ---
# In your loginSignup/views.py

try:
    # ... (os.path.join and settings.BASE_DIR setup)
    MODEL_DIR = os.path.join(settings.BASE_DIR, 'loginSignup', 'ml_models')

    loaded_pipeline = joblib.load(os.path.join(MODEL_DIR, 'job_role_model.pkl'))
    label_encoder = joblib.load(os.path.join(MODEL_DIR, 'label_encoder.pkl'))
    # --- ADD THIS LINE ---
    mlb_encoder = joblib.load(os.path.join(MODEL_DIR, 'mlb_encoder.pkl'))
    
    print("✅ All models and encoders loaded successfully.")
    
except FileNotFoundError as e:
    print(f"❌ FATAL ERROR: Could not find model files. {e}")
    loaded_pipeline = None

# --- Pre-define justifications for the roles ---
JOB_SCOPES = {
    'Software Engineer': "A high-demand role focused on designing and developing software. It offers strong career growth and is central to all modern industries.",
    'Data Scientist': "A rapidly growing field focused on extracting insights from data using machine learning and statistics to solve complex business problems.",
    'Mechanical Engineer': "A foundational engineering role that involves designing and manufacturing mechanical systems, from automotive to robotics.",
    'Accountant': "A stable profession ensuring the financial health of a business, with a clear path into financial management or consulting.",
    'HR': "A people-focused role crucial for shaping company culture, managing talent, and driving organizational success.",
    'Sales': "A dynamic role for driving revenue and building customer relationships, offering high earning potential and developing communication skills."
}

# ------------------ Save Prediction ------------------
# Replace your old save_prediction function with this one

# Replace your entire old function with this one

@login_required
def save_prediction(request):
    if request.method != "POST" or not loaded_pipeline:
        return JsonResponse({'error': 'Invalid request or model not loaded'}, status=400)

    try:
        data = json.loads(request.body)
        
        # --- 1. Prepare the non-skill data ---
        raw_input_data = {
            "degree": data.get("degree"),
            "major": data.get("major"),
            "cgpa": float(data.get("cgpa")),
        }

        # --- 2. Process and Encode the Skills correctly ---
        skills_list = [skill.strip().upper() for skill in data.get("skills", "").split(',')]
        encoded_skills = mlb_encoder.transform([skills_list])
        skills_df = pd.DataFrame(encoded_skills, columns=mlb_encoder.classes_)

        # --- 3. Create the final, complete DataFrame for the model ---
        input_df = pd.DataFrame([raw_input_data])
        final_df = pd.concat([input_df.reset_index(drop=True), skills_df.reset_index(drop=True)], axis=1)
        
        # --- 4. Run the prediction ---
        probabilities = loaded_pipeline.predict_proba(final_df)[0]
        class_names = label_encoder.classes_
        top_5_indices = np.argsort(probabilities)[::-1][:5]
        
        predictions = []
        for i in top_5_indices:
            role = class_names[i]
            score = probabilities[i]
            predictions.append({
                'role': role,
                'score': f"{score:.1%}",
                'scope': JOB_SCOPES.get(role, 'A promising field with opportunities.')
            })

        # --- 5. Save and Return ---
        PredHistory.objects.create(
            user=request.user,
            major=data.get("major", ""),
            cgpa=data.get("cgpa", None),
            degree=data.get("degree", ""),
            skills=data.get("skills", ""),
            year_of_graduation=data.get("yop", None),
            predicted_output=json.dumps(predictions)
        )

        return JsonResponse({
            "message": "Prediction successful!",
            "predictions": predictions
        })

    except Exception as e:
        print("❌ Error during prediction:", e)
        return JsonResponse({"error": str(e)}, status=500)


# ------------------ Fetch Prediction History (JSON API) ------------------
@login_required
def fetch_history(request):
    try:
        history_qs = PredHistory.objects.filter(user=request.user).order_by('-created_at')
        history = [
            {
                "major": h.major,
                "cgpa": float(h.cgpa) if h.cgpa else None,
                "degree": h.degree,
                "skills": h.skills.split(",") if h.skills else [],
                "year_of_graduation": h.year_of_graduation,
                "created_at": h.created_at.isoformat()
            } for h in history_qs
        ]
        return JsonResponse({"history": history})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ------------------ Home / Dashboard ------------------
@login_required
def home(request):
    return render(request, 'loginSignup/home.html', {"user": request.user})


# ------------------ Archive Page ------------------
# In your loginSignup/views.py

# Make sure 'json' is imported at the top of the file

# In your loginSignup/views.py

# Make sure 'json' is imported at the top of the file
# In your loginSignup/views.py

# Make sure 'json' is imported at the top of the file
# In loginSignup/views.py

# Make sure 'json' is imported at the top of the file
# In loginSignup/views.py
# In loginSignup/views.py
# In loginSignup/views.py

# In loginSignup/views.py

import json
from collections import Counter
import pandas as pd

@login_required
def archive(request):
    history_qs = PredHistory.objects.filter(user=request.user).order_by("-created_at")
    
    # --- Data preparation for both table and charts ---
    top_role_counts = Counter()
    
    # This loop is the FIX: It creates 'predictions_list' for the template
    for pred in history_qs:
        try:
            # Create the 'predictions_list' attribute that the template needs
            pred.predictions_list = json.loads(pred.predicted_output)
            if pred.predictions_list:
                # Also gather data for the top roles chart
                top_role_counts[pred.predictions_list[0]['role']] += 1
        except (json.JSONDecodeError, TypeError):
            # If data is bad, ensure the list is empty so the template doesn't crash
            pred.predictions_list = []
            
    # --- Chart data calculation ---
    chart1_labels = list(top_role_counts.keys())
    chart1_data = list(top_role_counts.values())

    history_data = list(history_qs.values('skills', 'degree', 'major', 'cgpa'))
    chart2_labels, chart2_data, chart3_labels, chart3_data = ([], [], [], [])
    if history_data:
        df = pd.DataFrame(history_data)
        
        # Chart 2: Skills Frequency
        all_skills = [s.strip() for skills in df['skills'].dropna() for s in skills.split(',') if s.strip()]
        skill_counts = Counter(all_skills).most_common(10)
        chart2_labels = [skill[0] for skill in skill_counts]
        chart2_data = [skill[1] for skill in skill_counts]

        # Chart 3: Average CGPA by Major
        df['cgpa'] = pd.to_numeric(df['cgpa'], errors='coerce')
        avg_cgpa = df.groupby('major')['cgpa'].mean().dropna().sort_values()
        chart3_labels = avg_cgpa.index.tolist()
        chart3_data = avg_cgpa.values.tolist()

    context = {
        "history": history_qs, # This queryset now has the .predictions_list attribute
        "chart1_labels": json.dumps(chart1_labels), "chart1_data": json.dumps(chart1_data),
        "chart2_labels": json.dumps(chart2_labels), "chart2_data": json.dumps(chart2_data),
        "chart3_labels": json.dumps(chart3_labels), "chart3_data": json.dumps(chart3_data),
    }
    return render(request, "loginSignup/archive.html", context)
# ------------------ Update Profile ------------------
@login_required
@csrf_exempt
def update_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
    try:
        data = json.loads(request.body)
        skills_csv = ",".join([s.strip() for s in data.get("skills", "").split(",") if s.strip()])

        last_prediction = UserPredictionHistory.objects.filter(user=request.user).order_by('-created_at').first()
        if last_prediction:
            last_prediction.major = data.get("major", last_prediction.major)
            last_prediction.cgpa = data.get("cgpa", last_prediction.cgpa)
            last_prediction.degree = data.get("degree", last_prediction.degree)
            last_prediction.skills = skills_csv
            last_prediction.year_of_graduation = data.get("yop", last_prediction.year_of_graduation)
            last_prediction.save()
            return JsonResponse({"message": "Profile updated successfully!"})
        else:
            UserPredictionHistory.objects.create(
                user=request.user,
                major=data.get("major", ""),
                cgpa=data.get("cgpa", None),
                degree=data.get("degree", None),
                skills=skills_csv,
                year_of_graduation=data.get("yop", None)
            )
            return JsonResponse({"message": "Profile saved successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ------------------ Get Latest Profile ------------------
@login_required
def get_latest_profile(request):
    try:
        last_prediction = UserPredictionHistory.objects.filter(user=request.user).order_by('-created_at').first()
        if last_prediction:
            return JsonResponse({
                "major": last_prediction.major,
                "cgpa": float(last_prediction.cgpa) if last_prediction.cgpa else None,
                "degree": last_prediction.degree,
                "skills": last_prediction.skills.split(",") if last_prediction.skills else [],
                "year_of_graduation": last_prediction.year_of_graduation
            })
        else:
            return JsonResponse({"message": "No profile found."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ------------------ Register ------------------
def register_user(request):
    SECRET_KEY = settings.SECRET_KEY
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                payload = {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'token': token, 'message': f'Welcome {user.username}!'})
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {field: error.get_json_data() for field, error in form.errors.items()}
                return JsonResponse({'errors': errors}, status=400)
            messages.error(request, 'Registration failed. Please correct the errors below.')
            return render(request, 'loginSignup/login.html', {'form': form, 'login_form': None})
    form = CustomUserCreationForm()
    return render(request, 'loginSignup/login.html', {'form': form, 'login_form': None})


# ------------------ Login ------------------
@csrf_exempt
def login_user(request):
    SECRET_KEY = settings.SECRET_KEY
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            payload = {'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'token': token, 'message': f'Welcome back, {user.username}!'})
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Invalid username or password.'}, status=400)
            messages.error(request, 'Invalid username or password.')
            return render(request, 'loginSignup/login.html', {'form': CustomUserCreationForm(), 'login_form': request.POST})
    return render(request, 'loginSignup/login.html', {'form': CustomUserCreationForm(), 'login_form': None})


# ------------------ Logout ------------------
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# ------------------ Test Preprocess ------------------
@csrf_exempt
def test_preprocess(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    try:
        raw_data = json.loads(request.body)
        processed = preprocess_input(raw_data)
        return JsonResponse({"processed_data": processed})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
