# Exchange Djongo 
My BTC exchange demo application, which can be tried on **[Heroku](https://exchange-django-mongodb.herokuapp.com)**. 

# Project Description 
Project build with python framework using Django. The platform has the following features: 
- Endpoint to manage user registration and access. 
- It automatically assigns each registered user a random amount of money and BTC. 
- Each user can sell BTC and buy BTC and the transactions are saved con MongoDB.
- Endpoint to get all active sell orders that are not matched yet. 
- Endpoint to see all users profits

# Technologies
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/) 
- [Django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [Django-Tailwind](https://django-tailwind.readthedocs.io/en/latest/)
- [Djongo](https://github.com/doableware/djongo) 
- [Whitenoise](http://whitenoise.evans.io/en/stable/) 
- [Guinicorn](https://docs.gunicorn.org/en/stable/run.html)

# Installation 
   -  Set a virtual environment
   - Install requirements.txt
   - Run migration excecuting with: 

> `python manage.py migrate` 

To run the Django development server and tailwind in dev mode, execute the following commands: 

> `python manage.py runserver` 

> `python manage.py tailwind start` 

Next, open the following URL in your browser: 

> `http://127.0.0.1:8000/`
