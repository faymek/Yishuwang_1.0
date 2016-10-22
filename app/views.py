"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest , HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from app.models import book
from django.template import RequestContext
from django.contrib import auth

from django import forms
class UserForm(forms.Form):
  email=forms.EmailField(label='email',max_length=50,widget=forms.TextInput(attrs={'size': 30,}))
  password1=forms.CharField(label='password',max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
  username=forms.CharField(label='username',max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
  password2= forms.CharField(label='Confirm',widget=forms.PasswordInput)


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    book_list_all = book.objects.all()
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'book_list_all':book_list_all,
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

# def register(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             password2 = form.cleaned_data['password2']
#         else:
#             form = UserForm()
#
#         user=User.objects.create_user(username, email, password)
#         user.save()
#         newUser = auth.authenticate(username=username, password=password)
#         if newUser is not None:
#             auth.login(request, newUser)
#             return HttpResponseRedirect("/")
#     else:
#         form= UserForm()
#         return render(request, "app/register.html", {'form': form})
#
#     return render(request, 'app/register.html')
def register(request):
    if request.method=='POST':
        errors=[]
        form=UserForm(request.POST)

        if not form.is_valid():
            return render(request, "app/register.html",{'form':form,'errors':errors})
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        password2= form.cleaned_data['password2']
        if password1!=password2:
            errors.append("两次输入的密码不一致!")
            return render(request, "app/register.html",{'form':form,'errors':errors})
        filterResult=User.objects.filter(username=username)
        if len(filterResult)>0:
           errors.append("用户名已存在")
           return render(request, "app/register.html",{'form':form,'errors':errors})
        user = User.objects.create_user(username,email,password1)
        user.save()
        #登录前需要先验证
        newUser=auth.authenticate(username=username,password=password1)
        if newUser is not None:
            auth.login(request, newUser)
            return HttpResponseRedirect("/")
    else:
        form =UserForm()
        return render(request, "app/register.html",{'form':form,'title':'注册','year':datetime.now().year})

    return render(request, "app/register.html")


class BookForm(forms.Form):
    name_book = forms.CharField(max_length=50)
    #年级的下拉框
    grade_choices = (
        ('大一上', '大一上'),
        ('大一下', '大一下'),
        ('大二上', '大二上'),
        ('大二下', '大二下'),
        ('大三上', '大三上'),
        ('大三下', '大三下'),
        ('大四上', '大四上'),
        ('大四下', '大四下'),
    )
    grade_book = forms.ChoiceField(choices=grade_choices)
    discount_choices =(
        ('1', '一折'),
        ('2', '二折'),
        ('3', '三折'),
    )
    discount_book = forms.ChoiceField(choices=discount_choices)

    major_choice = (
        ('信息安全', '信息安全'),
        ('软件工程', '软件工程'),
        ('计算机', '计算机'),
    )

    major_book = forms.ChoiceField(choices=major_choice)
    photo_book = forms.FileField()


def upload_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            name = book_form.cleaned_data['name_book']
            grade = book_form.cleaned_data['grade_book']
            discount = book_form.cleaned_data['discount_book']
            major = book_form.cleaned_data['major_book']
            photo =book_form.cleaned_data['photo_book']
            # acquire courrent user
            user = request.user
            book = user.book_set.create(name_book=name, grade_book=grade, discount_book=discount, major_book=major,
                                        photo_book=photo)
            book.save()
            return HttpResponseRedirect('/user_book_detail')
        else:
            book_form = BookForm()
            return HttpResponseRedirect('/upload_book')
    else:
        book_form = BookForm()
        return render(request, "app/upload_book.html", {'book_form': book_form,'title':'发布旧书','year':datetime.now().year})


def user_book_detail(request):
    user = request.user
    upoladed_book = user.book_set.all()
    context = {'uploaded_book_list':upoladed_book,
               'title': '我的书籍',
               'year': datetime.now().year,
               }
    return render(request,'app/user_book_detail.html',context)