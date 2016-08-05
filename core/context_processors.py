from core.forms import UserInformationForm


def user_information_form(request):
    data = {}

    if request.user.is_authenticated():
        data.update(
            email=request.user.email,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
        )
    return {
        'user_information_form': UserInformationForm(data=data)
    }
