import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, Comment, User

import random

from datetime import datetime

def populate():

    users = [
        {'username':'Mawaan', 'firstname':'Mawaan','lastname':'test','password':'Mawaan','email':'mawaan@test.com'},
        {'username':'Lisa', 'firstname':'Lisa','lastname':'test','password':'Lisa','email':'lisa@test.com'},
        {'username':'Willem', 'firstname':'Willem','lastname':'test','password':'Willem','email':'willem@test.com'}
    ]

    python_pages = [
        {'title':'Official Python Tutorial','url':'http://docs.python.org/3/tutorial/'},
        {'title':'How to Think like a Computer Scientist','url':'http://www.greenteapress.com/thinkpython/'},
        {'title':'Learn Python in 10 Minutes','url':'http://www.korokithakis.net/tutorials/python/'}
    ]

    django_pages = [
        {'title':'Official Django Tutorial','url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title':'Django Rocks','url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django','url':'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
        {'title':'Bottle','url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask','url':'http://flask.pocoo.org'}
    ]

    python_comments = [{'text':'I don\'t like Python, I prefer C++!', 'username':'Mawaan', 'date_added':datetime(2021,5,21,9,20,6)},
                        {'text':'I disagree with Mawaan, Python is so powerful', 'username':'Willem', 'date_added':datetime(2021,5,21,9,21,6)}
    ]
    django_comments = [{'text':'My students love Django so far.', 'username':'Lisa', 'date_added':datetime(2021,6,21,5,30,6)}
    ]
    other_pages_comments = [{'text':'There are so many approaches to Web Development!', 'username':'Willem', 'date_added':datetime(2021,4,22,3,21,8)}
    ]

    cats = {'Python':{'pages':python_pages, 'comments':python_comments, 'views':128,'likes':64},
            'Django':{'pages':django_pages, 'comments':django_comments, 'views':64,'likes':32},
            'Other Frameworks':{'pages':other_pages, 'comments':other_pages_comments, 'views':32,'likes':16}
            }

    for user in users:
        u = add_user(user['username'], user['firstname'], user['lastname'], user['password'], user['email'])

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])

        for p in cat_data['pages']:
            add_page(c,p['title'], p['url'])

        for cm in cat_data['comments']:
            add_comment(c, cm['username'], cm['text'], cm['date_added'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = random.randint(1,100)
    p.save()
    return p

def add_cat(name, views = 0, likes = 0):
    c = Category.objects.get_or_create(name=name, likes=likes, views=views)[0]
    c.save()
    return c

def add_user(username, firstname, lastname, password, email):
    u = User.objects.get_or_create(username=username)[0]
    u.first_name = firstname
    u.last_name = lastname
    u.email = email
    u.set_password(password)
    u.save()
    return u

def add_comment(cat, username, text, datetime):
    user = User.objects.get(username=username)
    cm = Comment.objects.get_or_create(category = cat, text = text, date_added=datetime, user=user)[0]
    cm.save()
    return cm

#Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()