from django.utils.text import slugify
from myapp.models import Post
# import re
# from googletrans import Translator, LANGUAGES
# from .sentiment import sent_pipeline
# trans = Translator()


#Hàm xử lý trùng lặp slug
def generate_unique_slug(title):
  base_slug = slugify(title)
  slug = base_slug
  num = 1
  while Post.objects.filter(slug=slug).exists():
      slug = f"{base_slug}-{num}"
      num += 1
  return slug

#Hàm xử lý các thẻ và các chữ số được truyền vào
# def clean_text(text):
#   clean = re.compile('<.*?>')
#   return re.sub(clean, '', text)

# #Hàm xử lý cảm xúc của bài viết
# def check_text(text):
#   trans_text = trans.translate(text=text, src='vi', dest='en').text
#   result = sent_pipeline(trans_text)
#   label = result[0]['label']
#   return label