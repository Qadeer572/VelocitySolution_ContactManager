from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from users.forms import CustomeUserRegistrationForm
from contact.models import Contact,Catagory




# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Now it uses Django's login()
            return redirect('/')
    else:
        form=AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = CustomeUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            current_user=User.objects.get(username=form.cleaned_data['username'])
            Catagory.objects.create(name='Other', user=current_user)
            return redirect('/login')  # redirect to login after successful signup
    else:
        form = CustomeUserRegistrationForm()
    return render(request, 'users/signup.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')
     
