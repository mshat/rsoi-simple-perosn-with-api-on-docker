from django.urls import path
from . import views


urlpatterns = [
    path('persons', views.PersonListView.as_view()),
    path('persons/<int:pk>', views.PersonView.as_view())
]