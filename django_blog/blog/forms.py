from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from taggit.forms import TagWidget, TagField
from taggit.models import Tag
from .models import Post, Profile, Comment

# User Forms
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

# Post Forms with TagWidget and tags field
class PostCreateForm(forms.ModelForm):
    """Form for creating posts with taggit tags"""
    # Add tags field using TagField and TagWidget
    tags = TagField(
        required=False,
        widget=TagWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas',
            'data-role': 'tagsinput'
        }),
        help_text="Enter tags separated by commas (e.g., django, python, web development)"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 15
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief summary of your post (optional)',
                'rows': 3,
                'maxlength': '300'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'title': 'Enter a descriptive title for your post (max 200 characters)',
            'content': 'Write the main content of your blog post',
            'excerpt': 'A brief summary that will appear in post listings (max 300 characters)',
        }
    
    def clean_tags(self):
        """Clean and validate tags"""
        tags = self.cleaned_data.get('tags', [])
        # Validate each tag
        for tag in tags:
            if len(tag) > 50:
                raise forms.ValidationError(f"Tag '{tag}' is too long (max 50 characters)")
            if len(tag) < 2:
                raise forms.ValidationError(f"Tag '{tag}' is too short (min 2 characters)")
        return tags

class PostUpdateForm(forms.ModelForm):
    """Form for updating posts with taggit tags"""
    # Add tags field using TagField and TagWidget
    tags = TagField(
        required=False,
        widget=TagWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas'
        }),
        help_text="Enter tags separated by commas"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

# Search Form
class SearchForm(forms.Form):
    """Form for searching posts"""
    q = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts...',
            'aria-label': 'Search'
        }),
        label='',
        help_text='Search by title, content, or tags'
    )
    
    search_in = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('title', 'Title'),
            ('content', 'Content'),
            ('tags', 'Tags'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        initial=['title', 'content', 'tags'],
        label='Search in:'
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('relevance', 'Relevance'),
            ('date', 'Date (Newest)'),
            ('date_old', 'Date (Oldest)'),
            ('title', 'Title (A-Z)'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        initial='relevance',
        label='Sort by:'
    )
    
    def clean_q(self):
        """Validate search query"""
        query = self.cleaned_data.get('q', '').strip()
        if len(query) < 2:
            raise forms.ValidationError("Search query must be at least 2 characters long")
        if len(query) > 100:
            raise forms.ValidationError("Search query is too long (max 100 characters)")
        return query

# Comment Forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3,
                'maxlength': '2000',
            }),
        }
        labels = {'content': ''}
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise forms.ValidationError("Comment must be at least 3 characters long.")
        return content

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': '2000',
            }),
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise forms.ValidationError("Comment must be at least 3 characters long.")
        return content

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your reply...',
                'rows': 2,
                'maxlength': '1000',
            }),
        }
        labels = {'content': ''}
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 3:
            raise forms.ValidationError("Reply must be at least 3 characters long.")
        return content
