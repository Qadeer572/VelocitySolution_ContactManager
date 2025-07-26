from django.shortcuts import render

# Create your views here.
def myContact(request):
    return render(request, 'contact/contact.html')

def dashboard(request):
    return render(request, 'contact/dashboard.html')


def addContact(request):
    if request.method == 'POST':
        print("Hello World")
    return render(request, 'contact/add_contact.html')