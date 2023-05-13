from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError


from django.utils.translation import gettext_lazy as _
# Create your models here.




class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return f'Comment by {self.author.username}'
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']



    
class UserRegistrationForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLogin(AuthenticationForm):
    pass