import hashlib
import time

from django.core.paginator import Paginator
from django.urls import reverse
from uuid import uuid4
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page


# Create your views here.
from mainapp.models import User, Blog, Replay


def md5pass(str):
    md5 = hashlib.md5()
    md5.update((str+'fuck').encode())
    return md5.hexdigest()

#  登录模块
def login(req):
    if req.method=='GET':
        return render(req,'index.html')
    name = req.POST.get('username')
    passwd = md5pass(req.POST.get('password'))
    if not(name or passwd):
        return render(req, 'index.html', {'msg': '用户名或密码不能为空.'})
    qs = User.objects.filter(name=name,passwd=passwd)
    if not qs.exists():
        return render(req,'index.html',{'msg':'用户密码错误.'})
    user = qs.first()
    if user.token:
        return render(req,'index.html',{'msg':'用户已经登录.'})
    ip = req.META.get('REMOTE_ADDR')
    tm = time.time
    char = 'fu'+ip+str(tm)+user.name+'ck'
    md5 = hashlib.md5()
    md5.update(char.encode())
    token=md5.hexdigest()
    user.token=token
    user.save()
    resp = redirect('/bloglist')
    resp.set_cookie('token',token)
    return resp

#   注册模块
def regist(req):
    if req.method == 'GET':
        return render(req, 'regist.html')
    name = req.POST.get('username')
    passwd = md5pass(req.POST.get('password'))
    phone = req.POST.get('phone')
    photo = req.FILES['photos']
    print(photo)
    if not(name or passwd):
        return render(req,'regist.html',{'msg':'用户名和密码不得为空.'})
    user=User.objects.create(name=name,passwd=passwd,phone=phone if phone else '',photo=photo)
    return render(req,'regist.html',{'msg':'用户{}注册成功，稍后转跳至登录页面.'.format(user.name)})


def bloglist(req):
    datas=Blog.objects.all()
    # paginator=Paginator(datas,1)
    # page = paginator.page(page_num)
    return render(req,'blog_list.html',{'datas':datas})


def logout(req):
    token=req.COOKIES.get('token')
    if token:
        try:
            user= User.objects.get(token=token)
            user.token=''
            user.save()
            resp = render(req,'logout.html',{'msg':'退出成功'})
            resp.delete_cookie('token')
            return resp
        except:
            pass
    return render(req,'logout.html',{'msg':'退出失败，您可能还没有登录'})


def show(req,id):
    return render(req,'show.html',{'blog':Blog.objects.filter(id=id).last()})


def edit(req):
    if req.method=='GET':
            return render(req,'edit.html',{'data':Blog.objects.filter(id=req.GET.get('id')).last()})
    id = req.POST.get('id')
    title =req.POST.get('title')
    summary =req.POST.get('summary')
    content =req.POST.get('content')
    if id:
        Blog.objects.filter(id=id).update(title=title,summary=summary,content=content)
    else:
        loginUser=User.objects.filter(token=req.COOKIES.get('token')).last()
        Blog.objects.create(user_id=loginUser.id,title=title,summary=summary,content=content)
    return HttpResponse('<h4>操作成功</h4><a href="/bloglist">返回列表</a')


def addBlog(req):
    return render(req,'edit.html')


def replay(req):
    qs = User.objects.filter(token=req.COOKIES.get('token'))
    loginUserId = qs.last().id if qs.exists() else 1
    blog_id = req.POST.get('blog_id')
    content = req.POST.get('repaly_content')
    Replay.objects.create(user_id=loginUserId,blog_id=blog_id,content=content)
    return redirect(reverse('show',args=(blog_id,)))