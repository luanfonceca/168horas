from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from invitations.models import Invitation

from attendee.models import Attendee

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

    def populate_user(self, request, sociallogin, data):
        email = sociallogin.account.extra_data.get('email')
        user = User.objects.get(email=email)

        try:
            invite = Invitation.objects.get(email=email)
        except Invitation.DoesNotExist:
            pass
        else:
            activity = invite.activities.first()
            is_attendee = activity.attendees.filter(user=user).exists()

            if not is_attendee:
                Attendee.objects.create(
                    name=user.get_full_name(),
                    email=user.email,
                    cpf=user.profile.cpf,
                    activity=activity,
                    profile=user.profile
                )


def custom_user_display(user):
    return user.get_full_name()
