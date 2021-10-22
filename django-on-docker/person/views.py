from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Person
from .serializers import PersonSerializer


class PersonListView(APIView):
    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        person = {arg: request.data.get(arg) for arg in ['name', 'age', 'address', 'work']}

        serializer = PersonSerializer(data=person)
        if serializer.is_valid(raise_exception=True):
            person_saved = serializer.save()
            return Response(status=status.HTTP_201_CREATED, data="Created new Person",
                            headers={"Location": f"/api/v1/persons/{person_saved.id}"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid data")


class PersonView(APIView):
    def get(self, request, pk):
        try:
            person = get_object_or_404(Person.objects.all(), pk=pk)
            serializer = PersonSerializer(person)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Not found Person for ID")

    def delete(self, request, pk):
        person = get_object_or_404(Person.objects.all(), pk=pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data="Person for ID was removed")

    def patch(self, request, pk):
        try:
            person = get_object_or_404(Person.objects.all(), pk=pk)
            data = {arg: request.data.get(arg) for arg in ['name', 'age', 'address', 'work'] if request.data.get(arg)}
            serializer = PersonSerializer(instance=person, data=data, partial=True)
            if serializer.is_valid():
                person_saved = serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid data")
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Not found Person for ID")
