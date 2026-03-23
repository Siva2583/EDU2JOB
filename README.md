# EDU2JOB

A machine learning web application that predicts optimal job roles for students using a Calibrated Random Forest model. 

## Features

* Predicts job roles based on student academic profiles and skill sets, providing confidence percentages for the top matches.
* User authentication and registration.
* Built with a Random Forest classifier calibrated using Isotonic Regression for high-accuracy predictions.

## Machine Learning Model Details

* **Algorithm:** `RandomForestClassifier` wrapped in `CalibratedClassifierCV`.
* **Input Features:**
  * `degree` (e.g., B.Tech, MBA, M.Sc)
  * `major` (e.g., Computer Science, Mechanical, Civil, Business)
  * `cgpa` (Numerical rating)
  * `skills` (Multiple skills accepted, e.g., Python, SQL, Java, Data Structures)
* **Predicted Job Roles:**
  * Software Engineer
  * Manufacturing Engineer
  * Investment Banker
  * Embedded Systems Engineer
  * Financial Analyst
  * Mechanical Engineer
  * Data Scientist

## Tech Stack

* **Backend:** Django
* **Machine Learning:** scikit-learn, Pandas, NumPy, joblib
* **Database:** SQLite

## Project Structure

```text
edu2job/
├── edu2job/          
├── loginSignup/      
├── db.sqlite3        
├── manage.py         
├── job_role_model.pkl 
├── label_encoder.pkl  
├── feature_columns.pkl
└── README.md
```
INSTALLATIONS::
git clone [https://github.com/Siva2583/EDU2JOB.git](https://github.com/Siva2583/EDU2JOB.git)
cd EDU2JOB
python -m venv venv
venv\Scripts\activate
pip install django scikit-learn pandas numpy joblib
python manage.py migrate
python manage.py runserver
