from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        user.role = User.Role.USER
        user.is_active = True
        user.save()
        return user
