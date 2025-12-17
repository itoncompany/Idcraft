from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from RatingAndReviews.models import Feedback

from django.contrib import messages
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        # match your <textarea name="comments">
        comments = request.POST.get('comments')
        rating = request.POST.get('rating')

        if not comments or not rating:
            messages.error(request, "Please provide both rating and comment.")
            return redirect('home')  # or wherever your form is
            name = request.user.profile.get_full_name() if hasattr(
            request.user, 'profile') else request.user.username
            Feedback.objects.create(
            user=request.user,
            name=name,
            comments=comments,
            rating=rating,
            profile_image=request.user.profile.get_profile_picture_url(),
        )
        messages.success(request, "Thank you for your feedback!")
        return redirect('home')
