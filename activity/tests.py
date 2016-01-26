from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest
from model_mommy import mommy

from category.models import Category
from activity.models import Activity


class ActivityTest(WebTest):
    def setUp(self):
        self.user = mommy.make(User, username='admin')
        self.category = mommy.make(Category, title='Praesent nec nisl')

    def test_factory_create(self):
        '''
        Test that we can create an instance via our object factory.
        '''
        instance = mommy.make(Activity, categories=[self.category])
        self.assertTrue(isinstance(instance, Activity))

    def test_list_empty_view(self):
        '''
        Test that the list view returns at least our factory created instance.
        '''
        response = self.app.get(reverse('activity:list'))
        object_list = response.context['object_list']
        for category in object_list:
            self.assertEquals(category.activities.count(), 0)
            self.assertQuerysetEqual(category.activities.all(), [])

    def test_list_view(self):
        '''
        Test that the list view returns at least our factory created instance.
        '''
        mommy.make(Activity, title=u'Nunc nulla', categories=[self.category])
        response = self.app.get(reverse('activity:list'))
        object_list = response.context['object_list']
        for category in object_list:
            self.assertEquals(category.activities.count(), 1)
            self.assertQuerysetEqual(
                category.activities.all(), ['<Activity: Nunc nulla>'])

    def test_create_view(self):
        '''
        Test that we can create an instance via the create view.
        '''
        response = self.app.get(reverse('activity:create'), user='admin')
        title = 'Maecenas ullamcorper dui'
        self.assertFalse(Activity.objects.filter(title=title).exists())

        response.form['title'] = title
        response.form['categories'].checked = True
        response.form.submit().follow()

        instance = Activity.objects.get(title=title)
        self.assertTrue(Activity.objects.filter(title=title).exists())
        self.assertEqual(instance.title, title)
        self.assertEqual(instance.created_by, self.user.profile)
        self.assertQuerysetEqual(
            instance.categories.all(),
            ['<Category: Praesent nec nisl>'])

    def test_detail_view(self):
        '''
        Test that we can view an instance via the detail view.
        '''
        instance = mommy.make(Activity, categories=[self.category])
        response = self.app.get(instance.get_absolute_url())
        self.assertEqual(response.context['object'], instance)

    def test_update_view(self):
        '''
        Test that we can update an instance via the update view.
        '''
        instance = mommy.make(
            Activity,
            categories=[self.category],
            created_by=self.user.profile)
        response = self.app.get(instance.get_update_url())

        old_created_by = instance.created_by
        new_title = 'Donec sodales sagittis'
        response.form['title'] = new_title
        response.form.submit().follow()

        instance = Activity.objects.get(pk=instance.pk)
        self.assertEqual(instance.title, new_title)
        self.assertEqual(instance.created_by, old_created_by)
        self.assertQuerysetEqual(
            instance.categories.all(),
            ['<Category: Praesent nec nisl>'])

    def test_delete_view(self):
        '''
        Test that we can delete an instance via the delete view.
        '''
        instance = mommy.make(Activity, categories=[self.category])

        response = self.app.get(instance.get_delete_url())
        response = response.form.submit().follow()

        self.assertFalse(Activity.objects.filter(pk=instance.pk).exists())
