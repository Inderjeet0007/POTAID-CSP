from django import forms

from csp_app.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model= Image
        fields = ['name', 'imagefile']

class UpdateImage(forms.ModelForm):
    model = Image
    # the fields mentioned below become the entry rows in the update form
    fields = ['processingf', 'area', 'depth', 'no_of_pothole']