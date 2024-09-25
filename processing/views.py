from django.shortcuts import render, redirect
from .forms import PostForm, SectionForm, RequestForm
from django.contrib.auth.models import User
from myapp.models import Post, Comment
from .utils import generate_unique_slug
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q

# Create your views here.
def index(request):
  if request.user.groups.filter(name='Contributor').exists() or request.user.groups.filter(name='Approver').exists() or request.user.groups.filter(name='Editor').exists():
    title = 'CMS'
    user = User.objects.get(id = request.user.id)
    pending_list_count = Post.objects.filter(status='Chờ duyệt').count()
    confirmation_list_count = Post.objects.filter(status='Chờ đăng').count()
    list_edit_count = Post.objects.filter(status='Chờ sửa', updated_by=request.user).count()
    context = {'title': title,
               'user': user,
               'pending_list_count': pending_list_count,
               'confirmation_list_count': confirmation_list_count,
               'list_edit_count': list_edit_count}
    return render(request,'processing/pages/home.html', context)
  else:
    messages.warning(request, 'Không phận sự miễn vào')
    return redirect('home')

def create_section(request):
  if request.user.groups.filter(name='Approver').exists():
    title = 'Thêm danh mục bài đăng'
    form_cs = SectionForm()
    if request.POST:
      form_cs = SectionForm(request.POST) 
      if form_cs.is_valid():
        section = form_cs.save(commit=False)
        section.slug = slugify(section.title)
        section.save()
        messages.success(request, 'Tạo danh mục thành công')
      return redirect('pro-home')
    context = {'title': title,
               'form_cs': form_cs}
    return render(request, 'processing/pages/create_section.html', context)
  else:
    messages.warning(request, 'Không phận sự miễn vào')
    return redirect('home')

def pending_list(request):
  if request.user.groups.filter(name='Approver').exists():
    title = 'Danh sách chờ duyệt'
    posts = Post.objects.filter(status='Chờ duyệt')
    if request.POST:
      ids = request.POST.get('post-ids', '')  
      ids = [int(id.strip()) for id in ids.split(',') if id.strip().isdigit()]
      posts = posts.filter(id__in=ids)
      action = request.POST.get('action', '')
      if action == 'refuse':
        for post in posts:
          post.status = 'Từ chối'
          post.save()
        messages.success(request, 'Đã từ chối những bản nháp đã chọn')
        return redirect('pending-list')
    context = {'title': title,
               'posts': posts}
    return render(request, 'processing/pages/pending_list.html', context)
  
def list_edit(request):
  if request.user.groups.filter(name='Editor').exists():
    posts = Post.objects.filter(status = 'Chờ sửa', updated_by=request.user)
    title = 'Danh sách chờ chỉnh sửa'
    context = {'title': title,
               'posts': posts}
    return render(request, 'processing/pages/list_edit.html', context)
  else:
    messages.warning(request, 'Không phận sự miễn vào')
    return redirect('pro-home')
  
def draft_list(request, str):
  if request.user.username == str:
    title = f'Danh sách bài viết {request.user.username}'
    drafts = Post.objects.filter(Q(status='Chờ gửi')|Q(status='Từ chối'),created_by = request.user)
    status = ''
    if request.GET:
      status = request.GET.get('status', '')
      if status == 'Chờ gửi':
        drafts = drafts.filter(status = 'Chờ gửi')
      if status == 'Từ chối':
        drafts = drafts.filter(status = 'Từ chối')
    if request.POST:
      ids = request.POST.get('post-ids', '')  
      ids = [int(id.strip()) for id in ids.split(',') if id.strip().isdigit()]
      drafts = drafts.filter(id__in=ids)
      action = request.POST.get('action', '')
      if action == 'send':
        for draft in drafts:
          draft.status = 'Chờ duyệt'
          draft.save()
        messages.success(request, 'Đã gửi những bản nháp đã chọn')
        return redirect('draft-list', str=request.user)
      if action == 'delete':
        ids = request.POST.get('post-ids', '')  
        ids = [int(id.strip()) for id in ids.split(',') if id.strip().isdigit()]
        drafts = drafts.filter(id__in=ids)
        action = request.POST.get('action', '')
        for draft in drafts:
          draft.delete()
        messages.success(request, 'Đã xóa những bản nháp đã chọn')
        return redirect('draft-list', str=request.user)
    context = {'title':title,
               'drafts':drafts,
               'status': status}
    return render(request, 'processing/pages/draft_list.html', context)
  else:
    messages.warning(request, 'Không xâm phạm bài viết')
    return redirect('pro-home')
  
def draft_detail(request,str,slug):
  try:
    draft = Post.objects.get(Q(status='Chờ gửi')|Q(status='Từ chối'), slug=slug, created_by=request.user)
  except Post.DoesNotExist:
    draft = None
  if draft:
    title = f'Bản nháp của {str}'
    if request.POST:
      send = request.POST.get('send', '')
      delete = request.POST.get('delete', '')
      if delete:
        draft.delete()
        messages.success(request, 'Xóa bản nháp thành công')
        return redirect('pro-home')
      if send:
        draft.status = 'Chờ duyệt'
        draft.save()
        messages.success(request, 'Gửi bài thành công')
        return redirect('pro-home')
    context = {'draft': draft,
               'title': title}
    return render(request, 'processing/pages/draft_detail.html', context)
  else:
    messages.warning(request, 'Không tìm thấy bản nháp này')
    return redirect('pro-home')

def post_detail(request, int):
  try:
    post = Post.objects.get(id=int)
  except Post.DoesNotExist:
    post = None
  if post: 
    if request.user.groups.filter(name='Approver').exists() or request.user.groups.filter(name='Editor').exists():
      title = f'Bài viết số {int}'
      post = Post.objects.get(id=int)
      req_edits = post.post_request.all()
      editors = User.objects.filter(groups__name='Editor')
      form_rq = RequestForm()
      if request.POST:
        refuse = request.POST.get('refuse', '')
        editor_id = request.POST.get('editor-id', '')
        delete = request.POST.get('delete', '')
        start_time = request.POST.get('start-time', '')
        end_time = request.POST.get('end-time', '')
        content = request.POST.get('content', '')
        if delete:
          post.delete()
          messages.success(request, 'Xóa bài thành công')
        else:
          if refuse:
            post.status = 'Từ chối'
            post.save()
            messages.success(request, 'Đã từ chối bản nháp')
          elif editor_id:
            post.updated_by = User.objects.get(id=editor_id)
            post.status = 'Chờ sửa'
            post.save()
            form_rq = RequestForm(request.POST)
            if form_rq.is_valid():
              req_edit = form_rq.save(commit=False)
              req_edit.sender = request.user
              req_edit.receiver = post.updated_by
              req_edit.status = 'Chỉnh sửa'
              req_edit.post = post
              req_edit.save()
              messages.success(request, 'Đã duyệt bài viết và gửi yêu cầu')
          elif content:
            post.status = 'Chờ edit'
            post.save()
            form_rq = RequestForm(request.POST)
            if form_rq.is_valid():
              req_edit = form_rq.save(commit=False)
              req_edit.sender = request.user
              req_edit.receiver = post.updated_by
              req_edit.status = 'Sửa lại'
              req_edit.post = post
              req_edit.save()
              messages.success(request, 'Đã gửi yêu cầu sửa lại đến biên tập viên')
          else:
            if start_time and end_time:
              post.start_time = start_time
              post.end_time = end_time
              post.status = 'Đã đăng'
              post.save()  
            else: 
              post.status = 'Đã đăng'
              post.save()
            messages.success(request, 'Đăng bài thành công')
        return redirect('pro-home')
      context = {'title': title,
                'post': post,
                'editors': editors,
                'req_edits': req_edits,
                'form_rq': form_rq}
      return render(request, 'processing/pages/post_detail.html', context)
    else:
      messages.warning(request, 'Không phận sự miễn vào')
      return redirect('home')
  else:
    messages.info(request, 'Bài viết đã bị xóa')
    return redirect('pro-home')

def create_draft(request):
  if request.user.groups.filter(name='Contributor').exists():
    form_cp = PostForm() #Nhận form đăng bài từ forms.py
    title = 'Tạo bản thảo'
    if request.POST:#Nếu có yêu cầu đăng bài gửi về thì xử lý
      form_cp = PostForm(request.POST, request.FILES) 
      if form_cp.is_valid(): #Kiểm tra dữ liệu gửi về form có hợp lệ không
        post = form_cp.save(commit=False)#Lưu vào form
        post.slug = generate_unique_slug(post.title) #Xử lý trùng lặp slug
        post.created_by = request.user #Xét user cho bài đăng
        post.save() #Lưu bài đăng
        messages.success(request, 'Tạo bản nháp thành cônggg')       
        return redirect('pro-home')
    return render(request,'processing/pages/create_draft.html', {'title': title, 'form_cp': form_cp})
  else:
    return redirect('home')
  
def update_draft(request,str,slug):
  try:
    draft = Post.objects.get(slug=slug, created_by=request.user, status='Chờ gửi')
  except Post.DoesNotExist:
    draft=None
  if draft:
    title = f'Sửa bản nháp của {str}'
    form_up = PostForm(instance=draft) #Lấy form từ form đã lưu của bài post đó ra
    if request.POST: #Nếu có yêu cầu chỉnh sửa gửi về
      send = request.POST.get('send', '')
      if send:
        form_up = PostForm(request.POST, request.FILES, instance=draft)
        if form_up.is_valid(): #Lưu những chỉnh sửa vào model và form luôn
          draft = form_up.save(commit=False)
          draft.slug = generate_unique_slug(draft.title) #Cập nhật lại slug (Vì slug lấy theo title, nên khi sửa title cũng phải sửa slug)
          draft.status = 'Chờ duyệt'
          draft.save() 
          messages.success(request, 'Đã gửi bản nháp cho Tổng biên tập')
          return redirect('draft-list', str=request.user)
      else:
        form_up = PostForm(request.POST, request.FILES, instance=draft)
        if form_up.is_valid(): #Lưu những chỉnh sửa vào model và form luôn
          draft = form_up.save(commit=False)
          draft.slug = generate_unique_slug(draft.title) #Cập nhật lại slug (Vì slug lấy theo title, nên khi sửa title cũng phải sửa slug)
          draft.save() 
          messages.success(request, 'Đã lưu chỉnh sửa bản nháp')
          return redirect('draft-detail', str=str, slug=draft.slug) #Điều hướng qua bài đăng vừa chỉnh sửa
    return render(request, 'processing/pages/update_post.html', {'title': title ,'form_up': form_up})
  else:
    messages.warning(request, 'Không tìm thấy bản chỉnh sửa')
    return redirect('pro-home')
  
def update_post(request, int):
  try:
    post = Post.objects.get(id=int, updated_by=request.user, status='Chờ sửa')
  except Post.DoesNotExist:
    post=None
  if post:
    title = f'Sửa bài viết số {int}'
    form_up = PostForm(instance=post) #Lấy form từ form đã lưu của bài post đó ra
    if request.POST: #Nếu có yêu cầu chỉnh sửa gửi về
      turnon = request.POST.get('turnon', '')
      if turnon:
        form_up = PostForm(request.POST, request.FILES, instance=post)
        if form_up.is_valid(): #Lưu những chỉnh sửa vào model và form luôn
          post = form_up.save(commit=False)
          post.slug = generate_unique_slug(post.title) #Cập nhật lại slug (Vì slug lấy theo title, nên khi sửa title cũng phải sửa slug)
          post.status = 'Chờ đăng'
          post.save() 
          messages.success(request, 'Đã gửi bài viết cho Tổng biên tập')
          return redirect('list-edit') #Điều hướng qua bài đăng vừa chỉnh sửa
      else:
        form_up = PostForm(request.POST, request.FILES, instance=post)
        if form_up.is_valid(): #Lưu những chỉnh sửa vào model và form luôn
          post = form_up.save(commit=False)
          post.slug = generate_unique_slug(post.title) #Cập nhật lại slug (Vì slug lấy theo title, nên khi sửa title cũng phải sửa slug)
          post.save() 
          messages.success(request, 'Đã lưu chỉnh sửa')
          return redirect('pro-post-detail', int=int) #Điều hướng qua bài đăng vừa chỉnh sửa
    return render(request, 'processing/pages/update_post.html', {'title': title ,'form_up': form_up})
  else:
    messages.warning(request, 'Không tìm thấy bản chỉnh sửa')
    return redirect('pro-home')
  
def confirmation_list(request):
  if request.user.groups.filter(name='Approver').exists():
    title = 'Danh sách chờ đăng'
    posts = Post.objects.filter(status='Chờ đăng')
    if request.POST:
      ids = request.POST.get('post-ids', '')  
      ids = [int(id.strip()) for id in ids.split(',') if id.strip().isdigit()]
      posts = posts.filter(id__in=ids)
      action = request.POST.get('action', '')
      if action == 'delete':
        for post in posts:
          post.delete()
        messages.success(request, 'Xóa thành công các bài viết đã chọn')
        return redirect('confirmation-list')
      if action == 'post':
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        if start_time and end_time:
          for post in posts:
            post.status = 'Đã đăng'
            post.start_time = start_time
            post.end_time = end_time
            post.save()
        else:
          for post in posts:
            post.status = 'Đã đăng'
            post.save()
        messages.success(request, 'Đã đăng bài viết đã chọn lên trang chủ')
        return redirect('confirmation-list')
    context = {'title': title,
               'posts': posts}
    return render(request, 'processing/pages/confirmation_list.html', context)
  else:
    messages.warning(request, 'Không phận sự miễn vào')
    return redirect('home')