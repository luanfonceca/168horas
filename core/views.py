from vanilla import TemplateView, UpdateView

from core.mixins import PageTitleMixin, LoginRequiredMixin
from core.models import Profile


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update(index_page=True)
        return context


class Profile(PageTitleMixin, LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    page_title = 'Profile update'
    model = Profile
    fields = ('state', 'categories',)

    def get_object(self):
        return self.request.user.profile
