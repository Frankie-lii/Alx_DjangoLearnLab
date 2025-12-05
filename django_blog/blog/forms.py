from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Profile, Comment, CommentLike

# ... existing User and Post forms above ...

class CommentForm(forms.ModelForm):
    """Form for creating and updating comments"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3,
                'maxlength': 2000,
            }),
        }
        labels = {
            'content': '',
        }
    
    def clean_content(self):
        """Validate comment content"""
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise forms.ValidationError("Comment must be at least 3 characters long.")
        if len(content) > 2000:
            raise forms.ValidationError("Comment cannot exceed 2000 characters.")
        return content.strip()

class CommentUpdateForm(forms.ModelForm):
    """Form for updating existing comments"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 2000,
            }),
        }
    
    def clean_content(self):
        """Validate comment content"""
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise forms.ValidationError("Comment must be at least 3 characters long.")
        if len(content) > 2000:
            raise forms.ValidationError("Comment cannot exceed 2000 characters.")
        return content.strip()

class CommentReplyForm(forms.ModelForm):
    """Form for replying to comments"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your reply...',
                'rows': 2,
                'maxlength': 1000,
            }),
        }
        labels = {
            'content': '',
        }
