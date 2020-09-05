from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import TranslationText
from googletrans import Translator
import requests
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Image
# Create your views here.



def ocr_space_file(filename, overlay=False, api_key='c934bdeda988957', language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                            files={filename: f},
                            data=payload,
                            )
    return r.content.decode()

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def home(request):
    form=TranslationText()
    if request.method=='POST':
        form = TranslationText(request.POST,request.FILES)
        transtext='Sample Text'
        if form.is_valid():
            img=request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(img.name, img)
            uploaded_file_url = fs.url(filename)
            lang = form.cleaned_data['lang']
            test_file = ocr_space_file('D:/GHCICodeathon/aasha'+ uploaded_file_url, language='pol')
            json1=json.loads(test_file)
            json1=json1["ParsedResults"][0]["ParsedText"]

            t=Translator()
            transtext=t.translate(json1, dest=lang).text
            
            

            return render(request, 'translated.html',  {'transtext': transtext})
        
    return render(request, 'index.html',{'form': form})