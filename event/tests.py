from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_webtest import WebTest
from model_mommy import mommy

from category.models import Category
from event.models import Event


class EventTest(WebTest):
    def setUp(self):
        self.user = mommy.make(User, username='admin')
        self.category = mommy.make(Category, title='Praesent nec nisl')

    def test_factory_create(self):
        '''
        Test that we can create an instance via our object factory.
        '''
        instance = mommy.make(Event, categories=[self.category])
        self.assertTrue(isinstance(instance, Event))

    def test_list_empty_view(self):
        '''
        Test that the list view returns at least our factory created instance.
        '''
        response = self.app.get(reverse('event:list'))
        object_list = response.context['object_list']
        for category in object_list:
            self.assertEquals(category.events.count(), 0)
            self.assertQuerysetEqual(category.events.all(), [])

    def test_list_view(self):
        '''
        Test that the list view returns at least our factory created instance.
        '''
        mommy.make(Event, title=u'Nunc nulla', categories=[self.category])
        response = self.app.get(reverse('event:list'))
        object_list = response.context['object_list']
        for category in object_list:
            self.assertEquals(category.events.count(), 1)
            self.assertQuerysetEqual(
                category.events.all(), ['<Event: Nunc nulla>'])

    def test_create_view(self):
        '''
        Test that we can create an instance via the create view.
        '''
        response = self.app.get(reverse('event:create'), user='admin')
        title = 'Maecenas ullamcorper dui'
        self.assertFalse(Event.objects.filter(title=title).exists())

        response.form['title'] = title
        response.form['categories'].checked = True
        response.form.submit().follow()

        instance = Event.objects.get(title=title)
        self.assertTrue(Event.objects.filter(title=title).exists())
        self.assertEqual(instance.title, title)
        self.assertEqual(instance.created_by, self.user.profile)
        self.assertQuerysetEqual(
            instance.categories.all(),
            ['<Category: Praesent nec nisl>'])

    def test_detail_view(self):
        '''
        Test that we can view an instance via the detail view.
        '''
        instance = mommy.make(Event, categories=[self.category])
        response = self.app.get(instance.get_absolute_url())
        self.assertEqual(response.context['object'], instance)

    def test_update_view(self):
        '''
        Test that we can update an instance via the update view.
        '''
        instance = mommy.make(
            Event,
            categories=[self.category],
            created_by=self.user.profile)
        response = self.app.get(instance.get_update_url())

        old_created_by = instance.created_by
        new_title = 'Donec sodales sagittis'
        response.form['title'] = new_title
        response.form.submit().follow()

        instance = Event.objects.get(pk=instance.pk)
        self.assertEqual(instance.title, new_title)
        self.assertEqual(instance.created_by, old_created_by)
        self.assertQuerysetEqual(
            instance.categories.all(),
            ['<Category: Praesent nec nisl>'])

    def test_delete_view(self):
        '''
        Test that we can delete an instance via the delete view.
        '''
        instance = mommy.make(Event, categories=[self.category])

        response = self.app.get(instance.get_delete_url())
        response = response.form.submit().follow()

        self.assertFalse(Event.objects.filter(pk=instance.pk).exists())
