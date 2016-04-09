from django.contrib.auth import get_user_model

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)


def custom_user_display(user):
    return user.get_full_name()
