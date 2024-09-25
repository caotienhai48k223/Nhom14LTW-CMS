from django.shortcuts import render, redirect
from myapp.models import Post, Topic, User, Enjoy
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.db.models import Count, Min, Q
from .utils import generate_date_range
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def pm_home(request):
  if request.user.is_superuser:
    title = 'Dashboard'
    topics = Post.objects.values('topic__title').annotate(total_views=Sum('views')).order_by('total_views')
    df_label_topic = [topic['topic__title'] for topic in topics]
    df_topic = [topic['total_views'] for topic in topics]
    
    cnt_topic = Post.objects.values('topic__title').annotate(count_post = Count('id')).order_by('count_post')
    df_label_cnt_topic = [topic['topic__title'] for topic in cnt_topic]
    df_cnt_topic = [topic['count_post'] for topic in cnt_topic]
    
    enjoys = Enjoy.objects.values('post__topic__title').annotate(total_enjoys=Count('id')).order_by('total_enjoys')
    df_label_enjoy = [enjoy['post__topic__title'] for enjoy in enjoys]
    df_enjoy = [enjoy['total_enjoys'] for enjoy in enjoys]
    
    users = User.objects.values('profile__age_band').annotate(total_age_bands = Count('id')).order_by('total_age_bands')
    df_label_age_band = [user['profile__age_band'] for user in users]
    df_age_band = [user['total_age_bands'] for user in users]
    
    users = User.objects.values('profile__gender').annotate(total_genders = Count('id')).order_by('total_genders')
    df_label_gender = [user['profile__gender'] for user in users]
    df_gender = [user['total_genders'] for user in users]

    today = datetime.now().date()
    first_post_date = Post.objects.aggregate(Min('created_at'))['created_at__min'].date() if Post.objects.exists() else today
    first_user_date = User.objects.aggregate(Min('date_joined'))['date_joined__min'].date() if User.objects.exists() else today
    start_date = min(first_post_date, first_user_date)
    all_dates = generate_date_range(start_date, today)
    daily_posts = Post.objects.annotate(date=TruncDate('created_at')).values('date').annotate(total_posts=Count('id')).order_by('date')
    daily_posts_dict = {post['date']: post['total_posts'] for post in daily_posts}
    daily_users = User.objects.annotate(date=TruncDate('date_joined')).values('date').annotate(total_user=Count('id')).order_by('date')
    daily_users_dict = {user['date']: user['total_user'] for user in daily_users}
    df_time = []
    df_post = []
    df_user = []
      
    for date in all_dates:
        df_time.append(date.strftime('%Y-%m-%d'))
        df_post.append(daily_posts_dict.get(date, 0))
        df_user.append(daily_users_dict.get(date, 0))
    content = {'title': title, 
               'df_topic':df_topic, 
               'df_label_topic': df_label_topic, 
               'df_cnt_topic': df_cnt_topic,
               'df_label_cnt_topic': df_label_cnt_topic,
               'df_time': df_time, 
               'df_post': df_post, 
               'df_user': df_user, 
               'df_enjoy': df_enjoy,
               'df_label_enjoy': df_label_enjoy,
               'df_age_band': df_age_band,
               'df_label_age_band': df_label_age_band,
               'df_gender': df_gender,
               'df_label_gender': df_label_gender}
    return render(request,'admin/pages/home.html', content)
  else:
    return redirect('home')
  

def pm_post(request):
  if request.user.is_superuser:
    title = 'Bài viết'
    topics = Topic.objects.all()
    posts = Post.objects.filter(is_deleted=False).annotate(count_enjoy=Count('enjoys_by'))
    keyword = request.GET.get('keyword', '')
    topic_req = request.GET.get('topic', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    if keyword:
      posts = posts.filter(Q(slug__icontains = slugify(keyword))|Q(body__icontains=keyword))
    if topic_req:
      posts = posts.filter(topic__title=topic_req)
    if start_date and end_date:
      sd_ed = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
      ed_ed = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
      posts = posts.filter(created_at__range=[sd_ed, ed_ed])
    elif start_date:
      sd_ed = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
      ed_ed = timezone.make_aware(datetime.now())
      posts = posts.filter(created_at__range=[sd_ed, ed_ed])
    elif end_date:
      ed_ed = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
      posts = posts.filter(created_at__range=[posts.earliest('created_at').created_at, ed_ed])
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', '')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    query_params = request.GET.copy()
    if 'page' in query_params:
      query_params.pop('page')
    content = {'title': title,
               'topics': topics,
               'page_obj': page_obj,
               'keyword': keyword,
               'topic_req': topic_req,
               'start_date': start_date,
               'end_date': end_date,
               'query_params': query_params.urlencode()}
    return render(request, 'admin/pages/posts.html', content)
  else:
    return redirect('home')

def pm_user(request):
  if request.user.is_superuser:
    title = 'Người dùng'
    users = User.objects.exclude(username=request.user.username).annotate(count_enjoy=Count('enjoys'))
    keyword = request.GET.get('keyword', '')
    gender = request.GET.get('gender', '')
    age_band = request.GET.get('age-band', '')
    if keyword:
      keyword_ed = ''.join(slugify(keyword).split('-'))      
      users = users.filter(Q(username__icontains = keyword_ed)|Q(profile__nickname__icontains = keyword_ed))
    if gender:
      users = users.filter(profile__gender=gender)
    if age_band:
      users = users.filter(profile__ageband=age_band)
    paginator = Paginator(users, 2)
    page_number = request.GET.get('page', '')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    query_params = request.GET.copy()
    if 'page' in query_params:
      query_params.pop('page')
    content = {'title': title,
               'page_obj': page_obj,
               'age_band': age_band,
               'gender': gender,
               'keyword': keyword,
               'query_params': query_params.urlencode()}
    return render(request, 'admin/pages/users.html', content)