from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rango.models import Category, Page, Comment
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from datetime import datetime

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dict)
    return response

def about(request):

    context_dict={}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['comments'] = Comment.objects.filter(category = category).order_by('-date_added')

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
        context_dict['comments'] = None

    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form':form,'category':category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False #Indicates whether registration was successful

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        #if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() #save user form data to database

            user.set_password(user.password) #hash password
            user.save() #update user object

            profile = profile_form.save(commit=False) #Avoid saving immediately for integry reasons
            profile.user = user

            #If there is a profile picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] # set profile picture

            profile.save() #save UserProfile instance

            registered = True #registration was successful

        else:
            print(user_form.errors, profile_form.errors) #print errors or mistakes

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    #Render template based on context
    return render(request, 'rango/register.html', context = {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
    if request.method == "POST":

        #get supplied user credentials
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password) #verify if the user details are valid

        if user: #details are correct
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else: #account is inactive
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else: #most likely for GET request
        return render(request, 'rango/login.html')

@login_required()
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request): #obtain number of visits to the site

    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0: #more than day since last visit
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now()) #update last visit cookie

    else:
        request.session['last_visit'] = last_visit_cookie #set last visit cookie

    request.session['visits'] = visits #update/set visits cookie