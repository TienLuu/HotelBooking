from django import forms
from .models import Hotel, HotelImage


class HotelForm(forms.Form):
    name = forms.CharField(max_length=225)
    hotel_type_id = forms.ChoiceField()
    address = forms.CharField(max_length=255)
    star = forms.ChoiceField()
    utilities = forms.MultipleChoiceField()
    tags = forms.MultipleChoiceField()
    supertags = forms.MultipleChoiceField()

    class Meta:
        model = Hotel
        fields = ('name', 'hotel_type', 'address', 'star',
                  'utilities', 'tags', 'supertags')


class ImageForm(forms.Form):
    image = forms.ImageField(label='Image')

    class Meta:
        model = HotelImage
        fields = ('image', )
