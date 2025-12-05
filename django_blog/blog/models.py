from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
import os

class Category(models.Model):
    """Model for post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('category-posts', kwargs={'slug': self.slug})

class Tag(models.Model):
    """Model for post tags"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    """Model for blog posts"""
    # Post status choices
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    # Basic fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, 
                               help_text="Brief summary of the post")
    
    # Author and timestamps
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts',
        related_query_name='post'
    )
    published_date = models.DateTimeField(
        default=timezone.now,
        help_text="Date when the post was/will be published"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status and visibility
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    
    # Relationships
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['status']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.content[:297] + '...' if len(self.content) > 300 else self.content
        
        # Auto-generate meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.excerpt
        
        # Set published_date if status changes to published
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_absolute_url_by_slug(self):
        return reverse('post-detail-slug', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        words_per_minute = 200
        word_count = len(self.content.split())
        reading_time = max(1, word_count // words_per_minute)
        return reading_time
    
    @property
    def is_published(self):
        """Check if post is published"""
        return self.status == 'published'
    
    def get_related_posts(self, limit=3):
        """Get related posts by category and tags"""
        related_posts = Post.objects.filter(
            models.Q(category=self.category) |
            models.Q(tags__in=self.tags.all())
        ).exclude(
            pk=self.pk
        ).distinct().filter(
            status='published'
        )[:limit]
        return related_posts

class Comment(models.Model):
    """Model for post comments"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None
    
    def get_replies(self):
        """Get all replies to this comment"""
        return self.replies.filter(is_approved=True)

class Profile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/%d/', 
        blank=True, 
        null=True,
        default='profile_pics/default.png'
    )
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Social media links
    twitter = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    
    # User preferences
    email_notifications = models.BooleanField(default=True)
    display_name = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        # Delete old profile picture when updating
        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.profile_picture and old_profile.profile_picture != self.profile_picture:
                    if os.path.isfile(old_profile.profile_picture.path):
                        os.remove(old_profile.profile_picture.path)
            except Profile.DoesNotExist:
                pass
        
        # Set display name to username if not provided
        if not self.display_name:
            self.display_name = self.user.username
        
        super().save(*args, **kwargs)
    
    @property
    def post_count(self):
        """Get count of published posts by this user"""
        return self.user.posts.filter(status='published').count()
    
    @property
    def full_name(self):
        """Get user's full name"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username

class PostImage(models.Model):
    """Model for post images/gallery"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='post_images/%Y/%m/%d/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
        verbose_name = "Post Image"
        verbose_name_plural = "Post Images"
    
    def __str__(self):
        return f"Image for {self.post.title}"
    
    def delete(self, *args, **kwargs):
        """Delete image file when model is deleted"""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

class Like(models.Model):
    """Model for post likes"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']
        ordering = ['-created_at']
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Bookmark(models.Model):
    """Model for user bookmarks"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookmarks'
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='bookmarked_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'post']
        ordering = ['-created_at']
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

# Signal imports for profile creation
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when a new user is created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

@receiver(pre_delete, sender=Profile)
def delete_profile_picture(sender, instance, **kwargs):
    """Delete profile picture file when profile is deleted"""
    if instance.profile_picture and instance.profile_picture.name != 'profile_pics/default.png':
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)

@receiver(pre_save, sender=Post)
def validate_post_content(sender, instance, **kwargs):
    """Validate post content before saving"""
    if len(instance.content.strip()) < 10:
        raise ValidationError("Post content must be at least 10 characters long")
    
    if len(instance.title.strip()) < 3:
        raise ValidationError("Post title must be at least 3 characters long")

# Custom manager for published posts
class PublishedPostManager(models.Manager):
    """Custom manager for published posts"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

# Add custom manager to Post model
Post.published = PublishedPostManager()

# Utility functions
def get_published_posts():
    """Get all published posts"""
    return Post.objects.filter(status='published')

def get_featured_posts(limit=5):
    """Get featured published posts"""
    return Post.objects.filter(
        status='published', 
        is_featured=True
    ).order_by('-published_date')[:limit]

def get_recent_posts(limit=5):
    """Get recent published posts"""
    return Post.objects.filter(
        status='published'
    ).order_by('-published_date')[:limit]

def get_posts_by_category(category_slug, limit=10):
    """Get posts by category slug"""
    return Post.objects.filter(
        status='published',
        category__slug=category_slug
    ).order_by('-published_date')[:limit]

def get_posts_by_tag(tag_slug, limit=10):
    """Get posts by tag slug"""
    return Post.objects.filter(
        status='published',
        tags__slug=tag_slug
    ).distinct().order_by('-published_date')[:limit]
