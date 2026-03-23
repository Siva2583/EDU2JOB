# EDU2JOB

A machine learning web application that predicts optimal job roles for students using a Random Forest model. 

## Features

* Predicts job roles based on student inputs.
* User authentication and registration.
* Built with a Random Forest classifier for high-accuracy predictions.

## Tech Stack

* Backend: Django
* Machine Learning: scikit-learn
* Database: SQLite

## Project Structure

```text
edu2job/
├── edu2job/          
├── loginSignup/      
├── db.sqlite3        
├── manage.py         
└── README.md


```
INSTALLATION STEPS::
git clone [https://github.com/Siva2583/EDU2JOB.git](https://github.com/Siva2583/EDU2JOB.git)
cd EDU2JOB
python -m venv venv
venv\Scripts\activate
pip install django scikit-learn pandas numpy
python manage.py migrate
python manage.py runserver
