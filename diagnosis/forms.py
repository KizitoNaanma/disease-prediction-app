from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # Remove field labels and help texts
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ""

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


# class PredictionForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         symptoms_dict = kwargs.pop('symptoms_dict', None)
#         num_fields = kwargs.pop('num_fields', 5)  # Default to 5 fields
#         super(PredictionForm, self).__init__(*args, **kwargs)
        
#         if symptoms_dict:
#             symptom_choices = [(key, key) for key in symptoms_dict.keys()]
#             for i in range(1, num_fields + 1):
#                 field_name = f'symptom_{i}'
#                 if field_name in self.fields:
#                     self.fields[field_name].choices = symptom_choices

#         # Add classes for Bootstrap styling
#         for field_name in self.fields:
#             self.fields[field_name].widget.attrs['class'] = 'form-control'
#             self.fields[field_name].widget.attrs['style'] = 'border-radius: 10px; padding: 10px; border: 1px solid #ced4da; font-size: 1rem;'

class PredictionForm(forms.Form):
    symptom_1 = forms.ChoiceField(choices=[])
    symptom_2 = forms.ChoiceField(choices=[])
    symptom_3 = forms.ChoiceField(choices=[])
    symptom_4 = forms.ChoiceField(choices=[])
    symptom_5 = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        symptoms_dict = kwargs.pop('symptoms_dict', None)
        super(PredictionForm, self).__init__(*args, **kwargs)
        
        if symptoms_dict:
            symptom_choices = [(key, key) for key in symptoms_dict.keys()]
            self.fields['symptom_1'].choices = symptom_choices
            self.fields['symptom_2'].choices = symptom_choices
            self.fields['symptom_3'].choices = symptom_choices
            self.fields['symptom_4'].choices = symptom_choices
            self.fields['symptom_5'].choices = symptom_choices

        
        # Add classes for Bootstrap styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

