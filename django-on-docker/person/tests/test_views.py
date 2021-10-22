from person.models import Person
from person.views import PersonListView, PersonView
from django.test import TestCase, Client
from rest_framework.generics import get_object_or_404
from django.http import Http404
from unittest.mock import Mock


client = Client()


class PersonViewTest(TestCase):
    def setUp(self):
        Person.objects.create(
            name='Curt', age=27, address='Aberdeen', work='Nirvana')
        Person.objects.create(
            name='Jimi', age=27, address='Melbourne', work='The Doors')
        self.person_view = PersonView()

    def test_get_single_person(self):
        person = Person.objects.get(name='Curt')
        response = self.person_view.get(None, person.pk)
        self.assertEqual(person.pk, response.data.get('id'))

    def test_get_non_exist_person(self):
        pk = 1000
        try:
            person = get_object_or_404(Person.objects.all(), pk=pk)
        except Http404:
            response = self.person_view.get(None, pk)
            self.assertEqual(404, response.status_code)
        else:
            raise self.fail('Person with this pk exists!')

    def test_delete(self):
        person = get_object_or_404(Person.objects.all(), name='Curt')
        assert person
        self.person_view.delete(None, person.pk)
        with self.assertRaises(Http404):
            get_object_or_404(Person.objects.all(), pk=person.pk)

    def test_patch(self):
        request = Mock()
        request.data = {'age': 100, 'work': 'test_work'}

        person = Person.objects.get(name='Curt')
        assert person.age != request.data.get('age')
        assert person.work != request.data.get('work')

        response = self.person_view.patch(request, person.pk)

        self.assertEqual(response.data.get('age'), request.data.get('age'))
        self.assertEqual(response.data.get('work'), request.data.get('work'))

    def test_patch_invalid_data(self):
        request = Mock()
        request.data = {'age': 'test_work', 'work': 100}

        person = Person.objects.get(name='Curt')
        assert person.age != request.data.get('age')
        assert person.work != request.data.get('work')

        response = self.person_view.patch(request, person.pk)

        self.assertEqual(400, response.status_code)

    def test_patch_not_found_person_for_ID(self):
        pk = 1000
        try:
            person = get_object_or_404(Person.objects.all(), pk=pk)
        except Http404:
            request = Mock()
            request.data = {'age': 'test_work', 'work': 100}

            response = self.person_view.patch(request, pk)
            self.assertEqual(404, response.status_code)
        else:
            raise self.fail('Person with this pk exists!')


