from django.db import models
from django.contrib.auth.models import User
from myapp.models import Post

# Create your models here.
class Request(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approver_comment')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_recipient')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_request')
  status = models.CharField(max_length=20, choices=[('Chỉnh sửa', 'Chỉnh sửa'), ('Sửa lại', 'Sửa lại')], default='Chỉnh sửa')
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'{self.sender.username} yêu cầu {self.receiver.username} {self.status} bài viết {self.post.id}'
  

  