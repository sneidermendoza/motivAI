from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

def get_token_google_oauth(strategy, details, user=None, *args, **kwargs):
    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        frontend_callback_url = "http://localhost:3000/auth/social/callback"
        redirect_url = f"{frontend_callback_url}?token={access_token}&refresh={refresh_token}"
        return redirect(redirect_url)
    else:
        error_redirect_url = "http://localhost:3000/auth/error"
        return redirect(error_redirect_url) 