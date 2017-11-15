# DjangoPrimer: minimum django(Django1.11.3)
this *.py contains what the minimum django needs
1. setting.py
2. urls.py
3. views.
4. WSGI service( recommend gunicorn on mac or linux)
5. cache

##Run by:
    python templateHello.py runserver 0.0.0.0:8000
##if you have installed Gunicorn, you can also run it by:
    gunicorn -w 6 -b 0.0.0.0:8000 templateHello --log-file=-