from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
# Create your views here.
# ------------------------------
# Logout View
# ------------------------------
def logout_view(request):
    logout(request)
    return redirect("/")
