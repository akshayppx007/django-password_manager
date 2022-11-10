from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from .forms import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home_page(request):
    return render(request, 'app/home.html')


def registration_page(request):
    form = RegisterForm(request.POST or None)
    if request.user.is_authenticated:
        messages.success(request, f"You are already logged in as {request.user}, returning to the home page")
        return redirect(home_page)
        
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
        if user != None:
            login(request, user)
            return redirect(user_pw_all)
        else:
            request.session['register_error'] = 1 
    context = {'form':form}        
    return render(request, 'app/register.html', context) 



def login_page(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        messages.success(request, f"You are already logged in as {request.user}, returning to the home page")
        return redirect(home_page)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect(user_pw_all)
        else:
            messages.warning(request, "credentials are not matching")
    context = {'form':form}
    return render(request, 'app/login.html', context)

@login_required(login_url=login_page)
def logged_out_page(request):
    logout(request)
    return render(request, 'app/logout.html')


@login_required(login_url=login_page)
def user_pw_all(request):
    message =''
    if request.user.authenticated:
        messages.success(request, f"Logged in as {request.user}")
    logged_in_user = request.user
    logged_in_user_pw = UserPW.objects.filter(user=logged_in_user) 
    if not logged_in_user_pw:
        message = 'please create a password'
        return message
    context = {'message':message, 'logged_in_user_pw':logged_in_user_pw}
    return render(request, 'app/user_pw_all.html', context)       


@login_required(login_url=login_page)
def edit(request, pk):
    user_post = UserPW.objects.get(id=pk)
    form = Userform()
    if request.method == 'POST':
        form = Userform(request.POST, instance=user_post)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'app/edit.html', context)




@login_required(login_url=login_page)
def delete(request, pk):
    user_post = User.objects.get(id=pk)
    if request.method == 'POST':
        user_post.delete()
        return redirect('/')

    context = {'user_post':user_post}
    return render(request, 'app/delete.html', context)    



@login_required(login_url=login_page)
def user_pw_add(request):
    form = UserPWForm(request.POST or None)
    if request.user.is_authenticated:
        messages.success(request, f"Logged in as {request.user}")
    logged_in_user = request.user
    if form.is_valid():
        title = form.cleaned_data.get('title')
        password = form.cleaned_data.get('password') 
        type = form.cleaned_data.get('type')
        if UserPW.objects.filter(title=title) and UserPW.objects.filter(user=request.user):
            messages.success(request, "There is a already a password created under that name") 
        else:
            try:
                UserPW.objects.create(title=title, password=password, type=type, user=logged_in_user)
                messages.success(request, "Password added successfully") 
            except Exception as e:
                raise e
    context = {'form':form}
    return render(request, 'app/user_pw_add.html', context)



@login_required(login_url=login_page)
def search(request):
    if request.user.is_authenticated:
        messages.success(request, f"Logged in as {request.user}")
    logged_in_user = request.user  
    logged_in_user_pws = UserPW.objects.filter(user=logged_in_user)
    if request.method == "POST":
        searched = request.POST.get("password_search", "")
        users_pws = logged_in_user_pws.values()
        if users_pws.filter(title=searched):
            user_pw = UserPW.objects.filter(Q(title=searched)).values()
            return render(request, "app/search.html", {'user_pw': user_pw})
        else:
            messages.error(request, "NOT FOUND")
   

    return render(request, "app/search.html", {'pws': logged_in_user_pws})


        


    





       



