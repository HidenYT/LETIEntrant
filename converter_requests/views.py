from django.shortcuts import render
from django import views
import requests
from .forms import TextSendForm
import json

class TextSendView(views.View):
    def get(self, request):
        form = TextSendForm()
        context = {
            'form': form,
        }

        return render(request, 'converter_requests/requests_page_template.html', context)

    def post(self, request):
        form = TextSendForm(request.POST or None)
        context = {
            'form': form, 
        }
        if form.is_valid():
            request_text = form.cleaned_data['text']
            convert_type = form.cleaned_data['file_format_choice']
            if convert_type == 'XML':
                response_text = requests.post(
                    'http://localhost:8000/converter/xmltojson/', 
                    data=request_text.encode('utf8'),
                    headers={'Content-type': 'application/xml'})
            elif convert_type == 'JSON':
                response_text = requests.post(
                    'http://localhost:8000/converter/jsontoxml/', 
                    json=json.loads(request_text),
                    headers={'Content-type': 'application/json'})
            response_text.encoding = 'utf8'
            context['response_text'] = response_text.text
        return render(request, 'converter_requests/requests_page_template.html', context)