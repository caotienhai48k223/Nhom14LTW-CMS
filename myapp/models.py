from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models.signals import post_save
from datetime import date

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  nickname = models.CharField(max_length=30, blank=True)
  avt = models.ImageField(upload_to='img', default='img/default-user.png')
  gender = models.CharField(max_length=20, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Ẩn', 'Ẩn')], default='Ẩn')
  dob = models.DateField(blank=True, null=True)
  age_band = models.CharField(max_length=10, choices=[('Ẩn', 'Ẩn'), ('18-30', '18-30'), ('31-45', '31-45'), ('46-65', '46-65'), ('65+', '65+')], default='Ẩn')
  about = models.CharField(max_length=1000)  
  
  def __str__(self):
    return self.user.username

  def calculate_age(self):
    if self.dob:
      today = date.today()
      age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
      if 18 <= age <= 30:
        return '18-30'
      elif 31 <= age <= 45:
        return '31-45'
      elif 46 <= age <= 65:
        return '46-65'
      elif age >= 66:
        return '65+'
    return 'Ẩn'
  
  def save(self, *args, **kwargs):
    if not self.nickname:
      self.nickname = self.user.username
    self.age_band = self.calculate_age()
    super(Profile, self).save(*args, **kwargs)
    
def create_profile(sender, instance, created, **kwargs):
  if created:
    user_profile = Profile(user=instance)
    user_profile.save()
post_save.connect(create_profile, sender=User)


class Topic(models.Model):
  title = models.CharField(max_length=30)
  slug = models.SlugField()
  
  def __str__(self):
    return self.title
 
  
class Section(models.Model):
  title = models.CharField(max_length=50)
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='section_topic')
  slug = models.SlugField()
  
  def __str__(self):
    return self.title


class Post(models.Model):
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_created')
  updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_updated', null=True, blank=True)
  title = models.CharField(max_length=500)
  image = models.ImageField(upload_to='img', default='img/default-img.jpg')
  body = CKEditor5Field('Text', config_name='extends')
  slug = models.SlugField(max_length=500)
  section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='post_section')
  views = models.IntegerField(default=0)
  status = models.CharField(max_length=20, choices=[('Chờ gửi', 'Chờ gửi'), ('Chờ duyệt', 'Chờ duyệt'),('Từ chối', 'Từ chối'), ('Chờ sửa', 'Chờ sửa'), ('Chờ đăng', 'Chờ đăng'), ('Đã đăng', 'Đã đăng')], default='Chờ gửi')
  start_time = models.TimeField(blank=True, null=True)
  end_time = models.TimeField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title
  

class Enjoy(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enjoys')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='enjoys_by')
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together=('user','post')
  
  def __str__(self):
    return f'user {self.user.id} enjoy post {self.post.id}'
  
class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_by')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
  content = models.CharField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'user {self.user.id} comment post {self.post.id} at {self.created_at}'