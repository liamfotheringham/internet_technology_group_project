from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View

from rango.models import Category, Page, Comment, UserProfile, Friend
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, CommentForm

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

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.category = Category.objects.get(slug=category_name_slug)
            comment.user = request.user
            comment.save()
        else:
            form = CommentForm()
        
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        form = CommentForm()

        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['comments'] = Comment.objects.filter(category = category).order_by('-date_added')
        context_dict['comment_form'] = form

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
        context_dict['comments'] = None
        context_dict['comment_form'] = None

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

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website':user_profile.website,
                                'picture':user_profile.picture})

        return(user, user_profile, form)

    def update_friend_status(self, request, session_user_profile, user_profile):
        if 'remove_friend' in request.POST:
            session_profile_friends = Friend.objects.get_or_create(user_profile=session_user_profile)[0]
            session_profile_friends.friends.remove(user_profile)

            user_profile_friends = Friend.objects.get_or_create(user_profile=user_profile)[0]
            user_profile_friends.friends.remove(session_user_profile)

        elif 'add_friend' in request.POST:

            session_profile_friends = Friend.objects.get_or_create(user_profile=session_user_profile)[0]
            session_profile_friends.friends.add(user_profile)

            user_profile_friends = Friend.objects.get_or_create(user_profile=user_profile)[0]
            user_profile_friends.friends.add(session_user_profile)


    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)

        except TypeError:
            return redirect(reverse('rango:index'))

        friends = get_five_friends(user_profile)

        if request.user.is_authenticated:
            all_session_friends = get_all_friends(request.user.userprofile)
            
            if(all_session_friends and user_profile in all_session_friends):
                is_friend = True
            else:
                is_friend = False
        else:
            is_friend = False


        context_dict = {'user_profile':user_profile,
                        'selected_user':user,
                        'form':form,
                        'friends':friends,
                        'is_friend':is_friend}
        
        return render(request, 'rango/profile.html', context_dict)
    
    def post(self, request, username):
        
        try:
            (user, user_profile, form) = self.get_user_details(username)

        except:
            return redirect(reverse('rango:index'))

        self.update_friend_status(request, request.user.userprofile, user_profile)

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

        friends = get_five_friends(user_profile)

        context_dict = {'user_profile':user_profile,
                        'selected_user':user,
                        'form':form,
                        'friends':friends}

        return render(request, 'rango/profile.html', context_dict)

def friends_list(request, username):
    context_dict = {}
    context_dict['username'] = username

    try:
        user = User.objects.get_or_create(username=username)[0]
        context_dict['friends'] = get_all_friends(user.userprofile)
    except:
        return redirect(reverse('rango:index'))
    
    return render(request, 'rango/friends_list.html', context_dict)

def get_five_friends(user_profile):
    try:
        friend = Friend.objects.get(user_profile=user_profile)
        return friend.friends.all()[:5]
        
    except Friend.DoesNotExist:
        return None

def get_all_friends(user_profile):
    try:
        friend = Friend.objects.get(user_profile=user_profile)
        return friend.friends.all()
        
    except Friend.DoesNotExist:
        return None

def check_username(request):
    if 'username' in request.GET:
        username = request.GET['username']
        print(username)

    try:
        username_exists = User.objects.get(username=username)
        username_exists = True

    except User.DoesNotExist:
        username_exists = False

    return render(request, 'rango/username_exists.html', {'username_exists': username_exists})

def search(request):
    """ search function """
    if request.method == "GET":
        query_name = request.GET.get('name', None)
        if query_name:
            results = Category.objects.filter(name__contains=query_name)
            return render(request, 'rango/search.html', {"results":results})
    return render(request, 'rango/search.html')