from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import PredictionForm, SignupForm
from .models import Prediction
import pickle
import numpy as np
from django.conf import settings
from openai import OpenAI
from django.conf import settings

import markdown
from django.utils.safestring import mark_safe


# openai.api_key = 'sk-Gy-WzCwuRHEKA5qACwKYURV8H45nxOLNdo25muXH3lT3BlbkFJYcKY4lvWw-IwgicUJjvaPQbzOPzgL3Yaj1Fn9QIUAA'
client = OpenAI()

def generate_remedies_with_openai(prediction):
    # prompt = f"Suggest possible remedies for {prediction}"
    
    # # Send the prompt to OpenAI
    # response = openai.completions.create(
    #     engine="text-davinci-003",  # You can choose other engines like 'gpt-3.5-turbo'
    #     prompt=prompt,
    #     max_tokens=100
    # )
    # # Extract the response text
    # return response['choices'][0]['text'].strip()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"The diagnosis is {prediction}. return the following in summary. a brief description, possible causes, some home remedies, what to do to curb spread or relief in the absence of medication. do not number the lines of the response"
        }
    ]
    )
    remedies_text = completion.choices[0].message.content
    print(remedies_text)
    # Convert markdown to HTML
    remedies_html = markdown.markdown(remedies_text)
    return mark_safe(remedies_html)

# Home view
def home(request):
    return render(request, 'home.html')

# Sign Up view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Prediction view
@login_required
# def predict_disease(request):
#     # Load model and data
#     with open(settings.BASE_DIR / 'diagnosis/mod2.pkl', 'rb') as f:
#         df = pickle.load(f)
#         rf_clf = pickle.load(f)
#         symptoms_dict = pickle.load(f)

#     num_fields = int(request.GET.get('num_fields', 5))  # Default to 5 fields

#     if request.method == 'POST':
#         form = PredictionForm(request.POST, symptoms_dict=symptoms_dict, num_fields=num_fields)
#         if form.is_valid():
#             input_vector = np.zeros(len(symptoms_dict))
#             selected_symptoms = []

#             for key, value in form.cleaned_data.items():
#                 if value in symptoms_dict:
#                     input_vector[symptoms_dict[value]] = 1
#                     selected_symptoms.append(value)

#             prediction = rf_clf.predict([input_vector])[0]

#             # Save the prediction result
#             Prediction.objects.create(
#                 user=request.user,
#                 symptoms=', '.join(selected_symptoms),
#                 prediction_result=prediction
#             )

#             return render(request, 'result.html', {'prediction': prediction})
#     else:
#         form = PredictionForm(symptoms_dict=symptoms_dict, num_fields=num_fields)

#     return render(request, 'predict.html', {'form': form})
def predict_disease(request):
    # Load model and data
    with open(settings.BASE_DIR / 'diagnosis/mod2.pkl', 'rb') as f:
        df = pickle.load(f)
        rf_clf = pickle.load(f)
        symptoms_dict = pickle.load(f)

    if request.method == 'POST':
        form = PredictionForm(request.POST, symptoms_dict=symptoms_dict)
        if form.is_valid():
            input_vector = np.zeros(len(symptoms_dict))
            selected_symptoms = []

            for key, value in form.cleaned_data.items():
                if value in symptoms_dict:
                    input_vector[symptoms_dict[value]] = 1
                    selected_symptoms.append(value)

            prediction = rf_clf.predict([input_vector])[0]
            # remedies = generate_remedies(prediction)
            remedies = generate_remedies_with_openai(prediction)

            # Save the prediction result
            Prediction.objects.create(
                user=request.user,
                symptoms=', '.join(selected_symptoms),
                prediction_result=prediction
            )

            return render(request, 'result.html', {'prediction': prediction, 'remedies': remedies})
    else:
        form = PredictionForm(symptoms_dict=symptoms_dict)

    return render(request, 'predict.html', {'form': form})

# Prediction history view

def add_symptom_field(request):
    num_fields = int(request.GET.get('num_fields', 5))
    symptoms_dict = {}
    # Load symptoms_dict here if needed
    with open(settings.BASE_DIR / 'diagnosis/mod2.pkl', 'rb') as f:
        symptoms_dict = pickle.load(f)

    form = PredictionForm(symptoms_dict=symptoms_dict, num_fields=num_fields + 1)
    
    # Render only the last field added
    last_field_name = f'symptom_{num_fields + 1}'
    last_field = form.fields[last_field_name]
    
    context = {
        'field': last_field,
        'field_name': last_field_name,
    }
    return render(request, 'partial_symptom_field.html', context)
@login_required
def prediction_history(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'history.html', {'predictions': predictions})
