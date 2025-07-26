from django.shortcuts import render,redirect
from contact.forms import ContactForm
from .models import Contact,Catagory
from datetime import datetime,date
from datetime import timedelta
from django.utils import timezone
# Create your views here.
def myContact(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(user=request.user)
        return render(request, 'contact/contact.html', {'contacts': contacts})
    return render(request, 'contact/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        Totalcontacts = Contact.objects.filter(user=request.user).count()
        TotalCategories = Catagory.objects.filter(user=request.user).count()
        dayContact = Contact.objects.filter(user=request.user, created_at__date=date.today()).count()
        weekContact = Contact.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=7)).count()
        monthContact = Contact.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=30)).count()
        recentAddition=Contact.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=30)).count()

        context={
            'Totalcontacts': Totalcontacts,
            'TotalCategories': TotalCategories,
            'dayContact': dayContact,
            'weekContact': weekContact,
            'monthContact': monthContact,
            'recentAddition': recentAddition
        }
        return render(request, 'contact/dashboard.html',{'context': context})
    return render(request, 'contact/dashboard.html')


def addContact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('contact')
        else:
            form= ContactForm(user=request.user)    
        return render(request, 'contact/addContact.html',{'form' : form})
    return render(request, 'contact/addContact.html')


def updateContact(request, contact_id):
    contact = Contact.objects.get(id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactForm(instance=contact, user=request.user)
    return render(request, 'contact/updateContact.html', {'form': form, 'contact': contact})