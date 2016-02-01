from django.utils.translation import ugettext as _
from django.shortcuts import redirect

from vanilla import TemplateView, UpdateView

from core.mixins import PageTitleMixin, LoginRequiredMixin
from core.models import Profile


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(index_page=True)
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('activity:list')


class ProfileView(PageTitleMixin, LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    page_title = _('Profile update')
    model = Profile
    fields = (
        'state', 'categories',
        'organizer_name', 'digital_signature', 'cpf', 'cnpj',
        'organizer_email', 'organizer_phone',
    )

    def get_object(self):
        return Profile.objects.get(user__id=self.request.user.id)
