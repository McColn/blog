from django import forms
from .models import *


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'birth_date', 'location', 'picture']
        widgets = {
            'name': forms.TextInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 100%; margin-bottom: 10px;',
                'placeholder': 'Enter title here'
            }),
            'bio': forms.TextInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 100%; margin-bottom: 10px;',
                'placeholder': 'Enter title here'
            }),
            'birth_date': forms.TextInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 100%; margin-bottom: 10px;',
                'placeholder': 'Enter title here'
            }),
            'location': forms.TextInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 100%; margin-bottom: 10px;',
                'placeholder': 'Enter title here'
            }),
            'picture': forms.ClearableFileInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 100%; margin-bottom: 20px;',
            }),
        }

class CommentForm(forms.ModelForm):
	comment = forms.CharField(
		label ='',
		widget=forms.Textarea(attrs={
			'rows': '2',
			'placeholder':'reply to post...'
			}))

	class Meta:
		model = Comment
		fields = ['comment']

# chat app ==========================
class ThreadForm(forms.Form):
	username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
	body = forms.CharField(label='', max_length=100)
	image = forms.ImageField(required=False)

	class Meta:
		model = MessageModel
		fields = ['body','image']
# end of chat app ==========================
	
# trial
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 80%; margin-bottom: 10px;',
                'placeholder': 'Enter title here'
            }),
            'content': forms.Textarea(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 100%; margin-bottom: 20px;',
                'placeholder': 'Enter title here'
            }),
            'image': forms.ClearableFileInput(attrs={
                'style': 'font-size: 12px; color: #333; border: 2px solid grey; padding: 7px; border-radius: 5px; width: 100%; margin-bottom: 20px;',
            }),
            'body': forms.Textarea(),
        }
        