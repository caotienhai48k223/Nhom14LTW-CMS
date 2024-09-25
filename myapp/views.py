from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, UpdateProfileForm, UpdateGroupForm
from .models import Post, Profile, Enjoy
from django.db.models import Q
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponse
from datetime import datetime


# Create your views here.
def register(request):
  # Nếu người dùng đã được đăng ký 
  if request.user.is_authenticated:
    return redirect('account')
  # Nếu chưa đăng ký thì mới đăng ký được 
  else:
    title = 'Đăng Ký'
    # Lấy form từ forms.py để truyền ra giao diện 
    form_signup = SignUpForm()
    # Nếu có yêu cầu đăng ký thì xử lý nó (Vì 1 form đăng ký hay đăng nhập sẽ đươc gửi lên = phương thức POST)
    if request.POST:
      # Tìm trong form đăng nhập xem có thông tin đó chưa 
      form_signup = SignUpForm(request.POST)
      # Nếu chưa thì lưu nó và đăng nhập luôn cho khách hàng 
      if form_signup.is_valid():
        user = form_signup.save() #Lưu thông tin vào model
        client_group = Group.objects.get(name='Client')
        user.groups.add(client_group)
        username = form_signup.cleaned_data['username'] #Chỉ lấy username để login
        password = form_signup.cleaned_data['password1'] #Chỉ lấy password1 để login
        user = auth.authenticate(username=username, password=password) #Lấy thông tin người dùng vừa đăng ký từ model
        auth.login(request, user) #Đăng nhập
        messages.success(request, 'Mở Tài Xỉu Thành Công') #Gửi thông báo ra giao diện
        return redirect('home')
      # Nếu có rồi thì báo lỗi cho khách hàng 
      else:
        messages.error(request, 'Có Vấn Đề Xảy Ra, Vui Lòng Thử Lại')
        return redirect('register')
    return render(request, 'client/pages/register.html', {'title': title ,'form_signup': form_signup})

def login(request):
  # Những người đã đăng nhập rồi thì không thể vào trang này, chuyển hướng ra tài khoản 
  if request.user.is_authenticated:
    return redirect('account')
  #Chưa đăng nhập thì hiện giao diện đăng nhập
  title = 'Đăng Nhập'
  # Nếu có yêu cầu đăng nhập thì giải quyết nó 
  if request.POST:
    username = request.POST.get('username') #Lấy ra tên đăng nhập
    password = request.POST.get('password') #Lấy ra mật khẩu
    user = auth.authenticate(username=username, password=password) #Kiểm tra xem user đã tồn tại chưa
    if user is not None: #Nếu có user thì login
      auth.login(request,user)
      return redirect('home')
    else: #Nếu chưa có user thì gửi thông báo ra giao diện
      messages.error(request,'Tài Khoản hoặc Mật Khẩu không đúng')
      return redirect('login')
  return render(request, 'client/pages/login.html', {'title': title})

#Đăng xuất, sử dụng tính năng có sẵn của django
def logout(request):
  auth.logout(request)
  return redirect('home')

def account(request, str):
  if request.user.is_authenticated:
    user = User.objects.get(username=str)
    title = f'{user.profile.nickname}'
    form_g = UpdateGroupForm(instance=user)
    if request.POST:
      form_g = UpdateGroupForm(request.POST, instance=user)
      if form_g.is_valid():
        form_g.save()
        messages.success(request,'Sửa quyền truy cập thành công')
        return redirect('home') 
    return render(request, 'client/pages/account.html', {'title': title, 'user': user, 'form_g': form_g})
  else:
    return redirect('login')

def index(request):
  title = 'The Da Nang Time'
  time_now = datetime.now().time()
  posts = Post.objects.filter(Q(start_time=None, end_time=None) | Q(start_time__lte=time_now, end_time__gte=time_now), status='Đã đăng')
  return render(request, 'client/pages/home.html', {'title': title, 'posts': posts})
  
def post_detail(request, str, slug):
  #Xét đăng nhập
  if request.user.is_authenticated:
    #Kiểm tra xem bài đăng có slug đó đã bị xóa chưa
    if not Post.objects.get(slug=slug).status == 'Đã đăng':
      messages.info(request, 'Bài viết đã bị xóa')
      return redirect('home')
    else:
      user = User.objects.get(username=str)
      title = f'Bài viết của {user.profile.nickname}' #str truyền vào là tên của chủ bài viết
      post = get_object_or_404(Post, user__username=str, slug=slug) #Tìm bài đăng đó
      post.views += 1 #Thêm 1 lượt truy cập
      post.save()
      post.is_enjoyed = False 
      posts_enjoy = request.user.enjoys.all()
      for post_enj in posts_enjoy:
        if post == post_enj.post:
          post.is_enjoyed = True
      posts_co_auth = Post.objects.filter(user__username=str).exclude(slug=slug) #Tìm những bài đăng cùng tác giả
      if post.topic:
        posts_co_topic = Post.objects.filter(topic=post.topic).exclude(slug=slug)
      else:
        posts_co_topic = Post.objects.filter(topic=None).exclude(slug=slug)
      #Nếu có yêu cầu xóa bài viết thì xử lý nó
      if request.POST:
        id_enjoy = request.POST.get('enjoy', '')
        post = Post.objects.get(id=id_enjoy)
        enjoy, created = Enjoy.objects.get_or_create(user=request.user, post=post)
        if not created:
          enjoy.delete()
          return JsonResponse({'status': 'removed'})
        else:
          return JsonResponse({'status': 'added'}) 
      return render(request, 'client/pages/post_detail.html', {'title': title, 'post':post, 'posts_co_auth': posts_co_auth, 'posts_co_topic': posts_co_topic})
  else:
    return redirect('login')

  
def update_profile(request, str):
  if request.user.username==str:
    title = f'Sửa hồ sơ {str}'
    form_u = UpdateUserForm(instance=request.user)
    form_p = UpdateProfileForm(instance=request.user.profile)
    if request.POST:
      form_u = UpdateUserForm(request.POST, instance=request.user)
      form_p = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
      if form_u.is_valid() and form_p.is_valid():
        form_u.save()
        form_p.save()
        messages.success(request, 'Cập nhật thông tin thành tài')
        return redirect('account', str=str)
    return render(request, 'client/pages/update_profile.html', {'title': title, 'form_u': form_u, 'form_p': form_p})
  else:
    return redirect('account', str=request.user.username)   

  
def enjoy_posts(request, str):
  if request.user.username == str:
    user = User.objects.get(username=str)
    title = f'Yêu thích {user.profile.nickname}'
    enjoys = user.enjoys.filter(post__is_deleted=False)
    return render(request,'client/pages/enjoy_posts.html', {'title': title, 'enjoys':enjoys})
  else:
    return redirect('account', str=request.user.username)
  
def search(request):
  keyword = request.GET.get('keyword', '')
  title = f"Tìm kiếm '{keyword}'"
  if keyword:
    posts = Post.objects.filter(Q(slug__icontains = slugify(keyword))|Q(body__icontains = keyword), is_deleted=False)
    return render(request, 'client/pages/search.html', {'title': title, 'keyword': keyword, 'posts': posts})
  else:
    return render(request, 'client/pages/search.html', {'title':title, 'keyword': keyword})
  