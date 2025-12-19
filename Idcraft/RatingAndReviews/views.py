from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from RatingAndReviews.models import Feedback


def submit_feedback(request):
    # Check authentication manually if you want a message before redirect
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to submit feedback.")
        return redirect('signin')

    if request.method == 'POST':
        comments = request.POST.get('comments')
        rating = request.POST.get('rating')

        # Validation
        if not comments or not rating:
            messages.error(request, "Please provide both rating and comment.")
            return redirect('home')

        # Get user name safely
        if hasattr(request.user, 'profile'):
            name = request.user.profile.full_name or request.user.username
            profile_image = request.user.profile.pr_pic
        else:
            name = request.user.username
            profile_image = None

        # Save feedback
        Feedback.objects.create(
            user=request.user,
            name=name,
            comments=comments,
            rating=rating,
            profile_image=profile_image
        )

        messages.success(request, "Thank you for your feedback!")
        return redirect('home')

    # Optional: prevent GET access
    messages.warning(request, "Feedback can only be submitted via the form.")
    return redirect('home')
