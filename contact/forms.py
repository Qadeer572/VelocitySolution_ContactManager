from django import forms
from .models import Contact, Catagory
from datetime import datetime

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'Catagory', 'address']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop user from kwargs
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['Catagory'].queryset = Catagory.objects.filter(user=self.user)

    def save(self, commit=True):
        contact = super().save(commit=False)
        contact.user = self.user
        if commit:
            contact.save()
        return contact
