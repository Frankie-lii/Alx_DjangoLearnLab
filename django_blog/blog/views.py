from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Count
from .models import Post, Profile, Comment, CommentLike
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm, 
    PostCreateForm, PostUpdateForm, CommentForm, 
    CommentUpdateForm, CommentReplyForm
)

# ... existing views above ...

# Comment Views

class CommentCreateView(LoginRequiredMixin, CreateView):
    """View for creating new comments"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Your comment has been posted successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['post_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        context['title'] = 'Add Comment'
        return context

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating comments"""
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Comment'
        context['post'] = self.object.post
        return context

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting comments"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Comment'
        return context

@login_required
def comment_like_toggle(request, pk):
    """Toggle like on a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.method == 'POST':
        like, created = CommentLike.objects.get_or_create(
            comment=comment,
            user=request.user
        )
        
        if not created:
            like.delete()
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'liked': created,
                'like_count': comment.likes.count()
            })
    
    return redirect('post-detail', pk=comment.post.pk)

@login_required
def comment_reply(request, pk):
    """Handle comment replies"""
    parent_comment = get_object_or_404(Comment, pk=pk)
    
    if request.method == 'POST':
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = parent_comment.post
            comment.author = request.user
            comment.parent = parent_comment
            comment.save()
            messages.success(request, 'Your reply has been posted!')
            return redirect('post-detail', pk=parent_comment.post.pk)
    else:
        form = CommentReplyForm()
    
    return redirect('post-detail', pk=parent_comment.post.pk)

def comment_list(request, post_pk):
    """View to list all comments for a post (for AJAX or API)"""
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.filter(
        parent__isnull=True,  # Only top-level comments
        is_approved=True
    ).order_by('-created_at')
    
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/comment_list.html', context)

# Update PostDetailView to include comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get top-level comments for this post
        comments = post.comments.filter(
            parent__isnull=True,
            is_approved=True
        ).order_by('-created_at').annotate(
            reply_count=Count('replies', filter=models.Q(replies__is_approved=True))
        )
        
        # Add comment form
        context['comment_form'] = CommentForm()
        context['comments'] = comments
        context['comment_count'] = post.comments.filter(is_approved=True).count()
        context['title'] = post.title
        
        # Track post views
        if self.request.user != post.author:
            post.increment_views()
        
        return context
