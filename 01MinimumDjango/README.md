# DjangoPrimer(Lightweight Django): Minimum Django(Django1.11.3)
This *.py contains what the minimum django needs
1. setting.py
2. urls.py
3. views.py
4. WSGI service( recommend gunicorn on mac or linux)

Run by

    python templateHello.py runserver 0.0.0.0:8000

if you have installed Gunicorn(recommend to use on linux or mac, ##pip install gunicorn), you can also run it by

    gunicorn -w 6 -b 0.0.0.0:8000 templateHello --log-file=-
    
Use templateHello as a minimum template, and create a new django project by :

    django-admin.py startproject foo --template=templateHello 