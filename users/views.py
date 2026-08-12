from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from flask import request
from .models import UserOTP
import random
from django.contrib.auth import get_user_model
User = get_user_model()
import os
import pickle
from django.conf import settings
MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models", "deploy_model.pkl")

ENCODER_PATH = os.path.join(settings.BASE_DIR, "ml_models", "label_encoder.pkl")

model = pickle.load(open(MODEL_PATH, "rb"))
label_encoder = pickle.load(open(ENCODER_PATH, "rb"))
 

 
from django.shortcuts import render
# ================================
# LOAD ML MODEL (USER SIDE)
# ================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml_models",
    "nids_multiclass_model.pkl"
)

with open(MODEL_PATH, "rb") as f:
    ml_data = pickle.load(f)

ml_model = ml_data["model"]
label_encoder = ml_data["label_encoder"]
features = ml_data["features"]
print("MODEL TYPE:", type(ml_model))
print("MODEL CLASSES:", ml_model.classes_)
print(dict(enumerate(label_encoder.classes_)))






# Create your views here.
def home_page(request):
    return render(request,'index.html')
def contact_page(request):
    return render(request,'contact.html')
def about_page(request):
    return render(request,'about.html')
def user_login_page(request):
    return render(request,'userLogin.html')


@csrf_exempt
def check_user_credentials(request):
    email = request.GET.get("email")
    password = request.GET.get("password")

    user = authenticate(username=email, password=password)
    if user:
        return HttpResponse("valid")
    return HttpResponse("invalid")
@csrf_exempt
def check_register_fields(request):
    email = request.GET.get("email")
    name = request.GET.get("name")
    mobile = request.GET.get("mobile")
    password = request.GET.get("password")

    if not all([email, name, mobile, password]):
        return HttpResponse("empty")

    if User.objects.filter(username=email).exists():
        return HttpResponse("exists")

    return HttpResponse("ok")


# ------------------ OTP SEND ------------------
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
import random
from .models import UserOTP


def user_send_otp(request):
    try:
        email = request.GET.get("email")
        if not email:
            return HttpResponse("failed")

        otp = str(random.randint(100000, 999999))

        # Put DB inside try
        UserOTP.objects.filter(email=email).delete()
        UserOTP.objects.create(email=email, otp=otp)
        print('otp is ',otp)
        send_mail(
            "Your OTP Verification",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return HttpResponse("sent")

    except Exception as e:
        print("OTP ERROR:", e)
        return HttpResponse("email_error")




# ------------------ OTP VERIFY ------------------
def user_verify_otp(request):
    email = request.GET.get("email")
    otp = request.GET.get("otp")

    if UserOTP.objects.filter(email=email, otp=otp).exists():
        UserOTP.objects.filter(email=email).delete()
        return HttpResponse("verified")

    return HttpResponse("invalid")


# ------------------ REGISTER ------------------
def user_register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            return render(request, "userLogin.html", {"error": "User already exists"})

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
            mobile=mobile,
            status="PENDING"     
        )

        return render(request, "userLogin.html", {"success": "Registration successful. Wait for admin approval."})


# ------------------ LOGIN ------------------
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user:
            # 👇 Status check
            if user.status == "APPROVED":
                login(request, user)
                return redirect('/user-dashboard/')
            elif user.status == "PENDING":
                return render(request, "userLogin.html", {
                    "error": "Your account is pending admin approval"
                })
            else:
                return render(request, "userLogin.html", {
                    "error": "Your account has been denied by admin"
                })

        return render(request, "userLogin.html", {"error": "Invalid Login Credentials"})
def user_dashboard(request):
    return render(request,'userDashboard.html')

def user_predict(request):
    return render(request,'user_predict.html')
def user_predict(request):
    print("DEBUG: predict_attack view called")

import os

import pickle
from django.conf import settings
from django.shortcuts import render
from .models import NetworkInput


import os
import pickle
import numpy as np

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import NetworkInput


 


# =====================================================
# USER PREDICTION VIEW
# =====================================================
@login_required
def user_predict(request):
    result = None
    confidence = None

    if request.method == "POST":
        try:
            # -------------------------------------------------
            # 1️⃣ READ INPUTS (MUST MATCH HTML name="")
            # -------------------------------------------------
            raw_inputs = {
                "Flow Duration": float(request.POST.get("flow_duration")),
                "Total Fwd Packets": float(request.POST.get("total_fwd_packets")),
                "Total Backward Packets": float(request.POST.get("total_bwd_packets")),
                "Fwd Packet Length Mean": float(request.POST.get("fwd_pkt_len_mean")),
                "Bwd Packet Length Mean": float(request.POST.get("bwd_pkt_len_mean")),
                "Packet Length Variance": float(request.POST.get("pkt_len_variance")),
            }

            # -------------------------------------------------
            # 2️⃣ ENFORCE TRAINING FEATURE ORDER
            # -------------------------------------------------
            features = [raw_inputs[name] for name in model.feature_names_]

            # -------------------------------------------------
            # 3️⃣ APPLY SAME PREPROCESSING AS TRAINING
            # -------------------------------------------------
            if getattr(model, "log_transform", False):
                features = np.log1p(features)

            # -------------------------------------------------
            # 4️⃣ PREDICT
            # -------------------------------------------------
            proba = model.predict_proba([features])[0]
            classes = label_encoder.classes_

            # collect attack probabilities (exclude BENIGN)
            attack_probs = {
                cls: p for cls, p in zip(classes, proba) if cls != "BENIGN"
            }

            # get most suspicious attack
            top_attack, top_prob = max(attack_probs.items(), key=lambda x: x[1])

            # 🔥 threshold-based decision
            THRESHOLD = 0.15   # you can tune this

            if top_prob >= THRESHOLD:
                result = top_attack
                confidence = round(top_prob * 100, 2)
            else:
                result = "BENIGN"
                confidence = round(max(proba) * 100, 2)


            # -------------------------------------------------
            # 5️⃣ SAVE TO DATABASE (OPTIONAL BUT GOOD)
            # -------------------------------------------------
            NetworkInput.objects.create(
                flow_duration=raw_inputs["Flow Duration"],
                total_fwd_packets=raw_inputs["Total Fwd Packets"],
                total_bwd_packets=raw_inputs["Total Backward Packets"],
                fwd_pkt_len_mean=raw_inputs["Fwd Packet Length Mean"],
                bwd_pkt_len_mean=raw_inputs["Bwd Packet Length Mean"],
                pkt_len_variance=raw_inputs["Packet Length Variance"],
                predicted_attack=result,
                confidence=confidence,
            )

        except Exception as e:
            result = "Error"
            confidence = None
            print("Prediction error:", e)

    return render(
        request,
        "user_predict.html",
        {
            "result": result,
            "confidence": confidence,
        }
    )


 






    


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def user_profile(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.mobile = request.POST.get("mobile")

        new_password = request.POST.get("new_password")
        if new_password:
            user.set_password(new_password)

        user.save()

        # ✅ set flag
        request.session['profile_updated'] = True
        return redirect("user_profile")

    # ✅ READ & REMOVE flag here
    profile_updated = request.session.pop('profile_updated', False)

    return render(request, "user_profile.html", {
        "profile_updated": profile_updated
    })
