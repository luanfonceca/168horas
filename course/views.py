from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from vanilla import model_views as views

from course.models import Course
from course.forms import CourseForm


class BaseCourseView(object):
    model = Course
    form_class = CourseForm
    lookup_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(BaseCourseView, self).get_context_data(**kwargs)
        if hasattr(self, 'page_title'):
            context.update(page_title=self.page_title)
        return context


class CourseList(BaseCourseView, views.ListView):
    template_name = 'course/list.html'
    queryset = Course.objects.all()
    page_title = _(u'Maecenas vestibulum')


class CourseCreate(BaseCourseView, views.CreateView):
    template_name = 'course/form.html'
    page_title = _(u'Aenean vulputate eleifend')


class CourseDetail(BaseCourseView, views.DetailView):
    template_name = 'course/detail.html'
    page_title = _(u'Vestibulum eu')


class CourseUpdate(BaseCourseView, views.UpdateView):
    template_name = 'course/form.html'
    page_title = _(u'Fusce ac felis')


class CourseDelete(BaseCourseView, views.DeleteView):
    template_name = 'course/delete.html'
    page_title = _(u'Fusce ac felis')
    # success_url = reverse('index')

    def get_success_url(self):
        return reverse('course:list')
