from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# ------------------------------
# Logout View
# ------------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect("/")


# ------------------------------
# Signup View
# ------------------------------
@csrf_protect
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check all fields
        if not all([username, email, password1, password2]):
            messages.error(request, "All fields are required")
            return redirect("signup")

        # Password match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # Check username/email
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        # Create inactive user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.is_active = False
        user.save()

        messages.success(
            request,
            "Account created successfully. Please wait for activation."
        )
        return redirect("/")

    return render(request, "MainApps/home.html")


# ------------------------------
# Signin View
# ------------------------------
@csrf_protect
def signin_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user exists
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("signin")

        # Authenticate
        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("signin")

        # Check if account active
        if not user.is_active:
            messages.warning(
                request,
                "Your account is not active yet. Please contact admin."
            )
            return redirect("signin")

        # Login active user
        login(
            request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )

        messages.success(
            request,
            "Login successful. Your account is active."
        )
        return redirect("home")

    return redirect("/")

def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        elif len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password changed successfully.")
            return redirect("home")  # or wherever you want

    return redirect("home")  # fallback redirect if GET