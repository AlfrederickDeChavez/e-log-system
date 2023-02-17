from django.forms import ModelForm
from .models import Bulletin

class BulletinForm(ModelForm):
    class Meta:
        model = Bulletin
        fields = '__All__'