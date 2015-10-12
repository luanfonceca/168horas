from django.core.urlresolvers import reverse

from django_webtest import WebTest
from model_mommy import mommy

from category.models import Category
from course.models import Course


class CourseTest(WebTest):
    def setUp(self):
        self.category = mommy.make(Category)

    def test_factory_create(self):
        '''
        Test that we can create an instance via our object factory.
        '''
        instance = mommy.make(Course, category=self.category)
        self.assertTrue(isinstance(instance, Course))

    def test_list_empty_view(self):
        '''
        Test that the list view returns at least our factory created instance.
        '''
        response = self.app.get(reverse('course:list'))
        object_list = response.context['object_list']
        self.assertEquals(object_list.count(), 0)
        self.assertQuerysetEqual(object_list, [])

    def test_list_view(self):
        '''
        Test that the list view returns at least our factory created instance.
        '''
        mommy.make(Course, title=u'Nunc nulla')
        response = self.app.get(reverse('course:list'))
        object_list = response.context['object_list']
        self.assertEquals(object_list.count(), 1)
        self.assertQuerysetEqual(object_list, ['<Course: Nunc nulla>'])

    def test_create_view(self):
        '''
        Test that we can create an instance via the create view.
        '''
        response = self.app.get(reverse('course:create'))
        title = 'Maecenas ullamcorper dui'
        self.assertFalse(Course.objects.filter(title=title).exists())

        response.form['title'] = title
        response.form.submit().follow()

        instance = Course.objects.get(title=title)
        self.assertTrue(Course.objects.filter(title=title).exists())
        self.assertEqual(instance.title, title)

    def test_detail_view(self):
        '''
        Test that we can view an instance via the detail view.
        '''
        instance = mommy.make(Course, category=self.category)
        response = self.app.get(instance.get_absolute_url())
        self.assertEqual(response.context['object'], instance)

    def test_update_view(self):
        '''
        Test that we can update an instance via the update view.
        '''
        instance = mommy.make(Course, category=self.category)
        response = self.app.get(instance.get_update_url())

        new_title = 'Donec sodales sagittis'
        response.form['title'] = new_title
        response.form.submit().follow()

        instance = Course.objects.get(pk=instance.pk)
        self.assertEqual(instance.title, new_title)

    def test_delete_view(self):
        '''
        Test that we can delete an instance via the delete view.
        '''
        instance = mommy.make(Course, category=self.category)

        response = self.app.get(instance.get_delete_url())
        response = response.form.submit().follow()

        self.assertFalse(Course.objects.filter(pk=instance.pk).exists())
