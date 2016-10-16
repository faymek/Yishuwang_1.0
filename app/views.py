"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.models import *
from django.template import RequestContext

from django import forms
class UserRegisterForm(forms.Form):
  email=forms.EmailField(label='e-mail',max_length=50,widget=forms.TextInput(attrs={'size': 30,}))
  password=forms.CharField(label='password',max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
  username=forms.CharField(label='username',max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
  password2= forms.CharField(label='Confirm',widget=forms.PasswordInput)
  def pwd_validate(self,p1,p2):
    return p1==p2


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def register(request):
    errors = []
    account = None
    password = None
    password2 = None
    email = None
    CompareFlag = False

    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('Please Enter username')
        else:
            account = request.POST.get('account')
        if not request.POST.get('email'):
            errors.append('Please Enter email')
        else:
            email = request.POST.get('email')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if not request.POST.get('password2'):
            errors.append('Please Enter password2')
        else:
            password2 = request.POST.get('password2')

        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else:
                errors.append('password2 is diff password ')


                # if account is not None and  email is not None and CompareFlag :
        user = User.objects.create_user(account, email, password)
        user.is_active = True
        user.is_staff = False
        user.save()
        return HttpResponseRedirect('/login')

    return render_to_response('app/register.html', {'errors': errors})