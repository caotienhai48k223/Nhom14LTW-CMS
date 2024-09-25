from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post, Topic, Profile


class UpdateUserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email')


class UpdateGroupForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('groups',) 


class UpdateProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['user', 'age_band']
    widgets = {'dob': forms.DateInput(attrs={'type': 'date'}),}


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Địa Chỉ Email'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Họ'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tên'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Tên Đăng Nhập'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Yêu cầu 150 ký tự trở xuống. Chỉ bao gồm chữ cái, số và @/./+/-/_ </small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Mật Khẩu'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Mật khẩu không được quá giống thông tin.</li><li>Mật khẩu phải hơn 8 ký tự.</li><li>Mật khẩu không được sử dụng phổ biến.</li><li>Mật khẩu không được toàn số.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Xác nhận Mật Khẩu'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Nhập lại mật khẩu để xác minh.</small></span>'