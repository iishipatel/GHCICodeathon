from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import TranslationText
from googletrans import Translator
import requests
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def ocr_space_url(url, overlay=False, api_key='c934bdeda988957', language='eng'):
    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


def home(request):
    form=TranslationText()
    if request.method=='POST':
        form = TranslationText(request.POST)
        transtext='Sample Text'
        if form.is_valid():
            # img=request.FILES['file']
            # fs = FileSystemStorage()
            # filename = fs.save(img.name, img)
            # uploaded_file_url = fs.url(filename)
            imgurl=form.cleaned_data['file']
            lang = form.cleaned_data['lang']
            # test_file = ocr_space_file('D:/GHCICodeathon/aasha'+ uploaded_file_url, language='pol')
            test_url = ocr_space_url(url=imgurl)
            json1=json.loads(test_url)
            json1=json1["ParsedResults"][0]["ParsedText"]

            t=Translator()
            transtext=t.translate(json1, dest=lang).text
            
            

            return render(request, 'translated.html',  {'transtext': transtext})
        
    return render(request, 'index.html',{'form': form})