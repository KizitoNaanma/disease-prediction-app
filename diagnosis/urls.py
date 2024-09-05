from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('predict/', views.predict_disease, name='predict_disease'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('add-symptom-field/', views.add_symptom_field, name='add_symptom_field'),

]
