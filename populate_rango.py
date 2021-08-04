import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, LikedCat, Page, Comment, User, UserProfile, Friend

import random

from datetime import datetime

def populate():
    SUPER_USER_USERNAME = "admin"
    SUPER_USER_PASSWORD = "admin"

    try:
        super_user = User.objects.create_superuser(SUPER_USER_USERNAME, "test@test.com", SUPER_USER_PASSWORD)
    except:
        pass



    mawaan_friends = ['Lisa', 'Willem']
    lisa_friends = ['Mawaan', 'Willem']
    willem_friends = ['Mawaan', 'Lisa']

    mawaan_likedcat = ['Python', 'Django']
    lisa_likedcat = ['Django', 'Other Frameworks']
    willem_likedcat = ['Python', 'Django', 'Other Frameworks']

    users = [
        {'username':'Mawaan', 'firstname':'Mawaan','lastname':'test','password':'Mawaan','email':'mawaan@test.com', 'website':'http://www.mawaan.com', 'friends':mawaan_friends, 'likedcats': mawaan_likedcat},
        {'username':'Lisa', 'firstname':'Lisa','lastname':'test','password':'Lisa','email':'lisa@test.com', 'website':'http://www.lisa.com', 'friends':lisa_friends, 'likedcats': lisa_likedcat},
        {'username':'Willem', 'firstname':'Willem','lastname':'test','password':'Willem','email':'willem@test.com', 'website':'http://www.willem.com', 'friends':willem_friends, 'likedcats': willem_likedcat}
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
        u = add_user(user['username'], user['firstname'], user['lastname'], user['password'], user['email'], user['website'])
        
    for user in users:
        f = add_friends(user['friends'], user['username'])

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])

        for p in cat_data['pages']:
            add_page(c,p['title'], p['url'])

        for cm in cat_data['comments']:
            add_comment(c, cm['username'], cm['text'], cm['date_added'])
        
    for user in users:
        if user['username'] == 'Mawaan':
            add_likedcat(user['username'], 'Python')
            add_likedcat(user['username'], 'Django')
        elif user['username'] == 'Lisa':
            add_likedcat(user['username'], 'Django')
            add_likedcat(user['username'], 'Other Frameworks')
        else:
            add_likedcat(user['username'], 'Python')
            add_likedcat(user['username'], 'Django')
            add_likedcat(user['username'], 'Other Frameworks')

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

    print(f"Super User Username: {SUPER_USER_USERNAME}")
    print(f"Super User Password: {SUPER_USER_USERNAME}")

def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = random.randint(1,100)
    p.save()
    return p

def add_cat(name, views = 0, likes = 0):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

def add_user(username, firstname, lastname, password, email, website):
    u = User.objects.get_or_create(username=username)[0]
    u.first_name = firstname
    u.last_name = lastname
    u.email = email
    u.set_password(password)
    u.save()

    up = UserProfile.objects.get_or_create(user=u)[0]
    up.website = website
    up.save()

    return u

def add_friends(friends, username):
    u = User.objects.get(username=username)
    up = UserProfile.objects.get(user=u)
    f = Friend.objects.get_or_create(user_profile=up)[0]

    for friend in friends:
        f_u = User.objects.get(username=friend)
        f_up = UserProfile.objects.get(user=f_u)
        f.friends.add(f_up)
        
    f.save()

    return f

def add_comment(cat, username, text, datetime):
    user = User.objects.get(username=username)
    cm = Comment.objects.get_or_create(category = cat, text = text, date_added=datetime, user=user)[0]
    cm.save()
    return cm

def add_likedcat(username, catname):
    u = User.objects.get(username=username)
    up = UserProfile.objects.get(user=u)
    lc = LikedCat.objects.get_or_create(user_profile=up)[0]
    cat = Category.objects.get(name=catname)
    cat.likes = cat.likes + 1
    cat.save()
    lc.likedcats.add(cat)
        
    lc.save()

    return lc

#Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()