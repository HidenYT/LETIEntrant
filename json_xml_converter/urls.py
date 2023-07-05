from django.urls import path
from .views import JSONtoXML, XMLtoJSON

urlpatterns = [
    path('jsontoxml/', JSONtoXML.as_view()),
    path('xmltojson/', XMLtoJSON.as_view()),
]