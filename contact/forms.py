from django import forms
from .models import Contact, Catagory,Activity
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
            contact.save()  # ✅ Save contact first
        return contact
    
class CatagoryForm(forms.ModelForm):
    class Meta:
        model = Catagory
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop user from kwargs
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.user:
            if Catagory.objects.filter(name__iexact=name, user=self.user).exists():
                raise forms.ValidationError("This category already exists for your account.")
        return name

    def save(self, commit=True):
        catagory = super().save(commit=False)
        catagory.user = self.user

        if commit:
            catagory.save()
        return catagory
