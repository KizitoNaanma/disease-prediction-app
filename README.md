# Disease Prediction System

An AI-powered web application developed using Django to predict diseases based on user-input symptoms. This system assists users in identifying potential health conditions early, promoting timely medical consultation.

## 🔧 Features

- **Symptom-Based Disease Prediction**: Users input symptoms to receive potential disease diagnoses.
- **Confidence Scoring**: Each prediction includes a confidence score to indicate the model's certainty.
- **User-Friendly Interface**: Intuitive web interface for seamless user experience.
- **Admin Dashboard**: Manage user data and system settings efficiently.

## 🧠 Machine Learning Model

- **Model**: Logistic Regression
- **Training**: Model trained using historical symptom-disease data 
- **Exported & Integrated**: The trained model is exported and integrated into the Django backend to perform symptom-based disease predictions.
- **Prediction Output**: Returns possible diseases along with confidence scores.

## 🛠️ Technical Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: Logistic Regression
- **Database**: SQLite (default), configurable to PostgreSQL or MySQL

## ⚙️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/KizitoNaanma/disease-prediction-app.git
   cd disease-prediction-app
2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    # On Linux/macOS
    source venv/bin/activate
    # On Windows
    venv\Scripts\activate

3. Install dependencies
   ```bash
   pip install -r requirements.txt
4. Apply database migrations
   ```bash
   python manage.py migrate
5. Run the development server
   ```bash
   python manage.py runserver
6. Access the application
   ```bash
   http://127.0.0.1:8000/
