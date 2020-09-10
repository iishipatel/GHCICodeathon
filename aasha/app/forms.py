from django import forms

class TranslationText(forms.Form):
    file = forms.CharField()
    lang = forms.ChoiceField(choices=[('bn','Bengali'),('gu','Gujarati'),('hi','Hindi'),('kn','kannada'),('ml','Malayalam'),('mr','Marathi'),('pa','Punjabi'),('sd','Sindhi'),('ta','Tamil'),('te','Telugu')])