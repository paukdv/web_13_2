from django.forms import ModelForm, CharField, TextInput
from .models import Author, Quote


class AddAuthor(ModelForm):
    fullname = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    born_date = CharField(min_length=10, required=True, widget=TextInput())
    born_location = CharField(min_length=10, required=True, widget=TextInput())
    description = CharField(min_length=10, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class AddQuote(ModelForm):
    quote = CharField(min_length=10, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']