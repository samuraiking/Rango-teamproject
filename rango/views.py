from django.shortcuts import render
from django.http import HttpResponse, response
from rango.models import Category, UserProfile
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import PageForm
from rango.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Welcame to our site!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    response=render(request, 'rango/index.html', context=context_dict)
    #visitor_cookie_handler(request)

    #request.session.set_test_cookie()
    

    return response

def about(request):
    context_dict = {}
    #if request.session.test_cookie_worked():
    #    print("TEST COOKIE WORKED!")
    #    request.session.delete_test_cookie()
    return render(request, 'rango/about.html')



def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)


@login_required
def register_profile(request):
    form = UserProfileForm()
    user_profile=UserProfile.objects.get_or_create(user=request.user)[0]
    user_profile.save()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,instance=user_profile)
    if form.is_valid():
        form.save()
        
        return redirect(reverse('rango:index'))
    else:
        print(form.errors)
    
    context_dict = {'form': form}
    return render(request, 'rango/profile_registration.html', context_dict)

'''
@login_required
def account_interface(request):
    cur_user=request.user
    userProfile=UserProfile.objects.filter(user=cur_user)[0]
    userForm=UserForm(instance=cur_user)
    userProfileForm=UserProfileForm(instance=userProfile)
    if request.method == 'POST' and userProfile:
        userProfileForm=UserProfileForm(request.POST, request.FILES,instance=userProfile)
    if userProfileForm.is_valid():
        userProfileForm.save()
        return redirect(reverse('rango:index'))
    
    

    context_dict = {"userForm":userForm,"userProfileForm":userProfileForm,'userProfile':userProfile}
    
    return render(request, 'rango/account_interface.html',context_dict)
'''
@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat=form.save(commit=True)
            #print(cat,cat.slug)
            return redirect('/rango/')
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors) 
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def search(request):
    result_list = []
    query=None
    if request.method == 'POST':
        query = request.POST['query'].strip()
    if query is not None:
        # Run our Bing function to get the results list!
        result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list': result_list})



@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')



def visitor_cookie_handler(request):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie =request.COOKIES.get('last_visit',str(datetime.now()))
    
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

<<<<<<< HEAD


class ProfileView(View):
    def get_user_details(self, username):
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
       
        form = UserProfileForm({'website': user_profile.website, 'picture': user_profile.picture})
        return (user, user_profile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        if(len(username)==0):
            username=request.user.username
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
        return render(request, 'rango/account_interface.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
            context_dict = {'user_profile': user_profile,
            'selected_user': user,
            'form': form}
        return render(request, 'rango/account_interface.html', context_dict)
=======
def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:# Run our Bing function to get the results list!
            result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list': result_list})

>>>>>>> e1dc1b2c02a730e85624d68f5f10bcb0336b4fef
