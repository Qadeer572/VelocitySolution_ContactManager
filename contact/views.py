from contact.forms import ContactForm,CatagoryForm
from .models import Contact,Catagory,Activity
from datetime import datetime,date
from datetime import timedelta
from django.utils import timezone
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Contact
from .forms import CatagoryForm

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def exportCatagoryContact(request):
    if not request.user.is_authenticated:
        return render(request, 'contact/catagory.html')  # anonymous users

    contact = Contact.objects.filter(user=request.user)

    context={
        'contact': contact,
        'user': request.user
    }
    form= CatagoryForm(user=request.user)
    return render(request, 'contact/exportContact.html', {
         'context': context,
    })

def export_catagory_pdf(request):
    # Get contacts for the current user
    contact = Contact.objects.filter(user=request.user).select_related('Catagory')
    
    # Debug print
    print(f"Contacts found: {contact.count()}")
    for c in contact:
        print(f"Contact: {c.name}, Category: {c.Catagory}")
    
    # Template path
    template_path = 'contact/exportContact.html'
    
    # Context with additional useful data
    context = {
        'contact': contact,
        'user': request.user,
        'request': request,  # Add request object
        'total_contacts': contact.count(),
    }
    
    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="categories.pdf"'
    
    # Get template and render with context
    template = get_template(template_path)
    html = template.render(context, request)  # Pass request as second parameter
    
    # Create PDF
    pisa_status = pisa.CreatePDF(
        src=html, 
        dest=response,
        encoding='UTF-8'  # Add encoding
    )
    
    # Check for errors
    if pisa_status.err:
        print(f"PDF generation error: {pisa_status.err}")
        return HttpResponse('Error generating PDF', status=500)
    
    return response


def catagoryContact(request):
    if not request.user.is_authenticated:
        return render(request, 'contact/catagory.html')  # anonymous users

    contact = Contact.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CatagoryForm(request.POST, user=request.user)
        if form.is_valid():
            catagory = form.save(commit=False)
            catagory.user = request.user
            catagory.save()
            messages.success(request, f"Category '{catagory.name}' created successfully.")
            return redirect('/catagoryContact/')  # use URL name instead of hardcoded path
    else:
        form = CatagoryForm(user=request.user)

    return render(request, 'contact/catagory.html', {
        'contact': contact,
        'form': form
    })


def myContact(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        contacts = Contact.objects.filter(user=request.user)

        # Apply search filter if query exists
        if query:
            contacts = contacts.filter(name__icontains=query) | contacts.filter(email__icontains=query)

        # Handle POST (Delete Contact)
        if request.method == "POST":
            contact_id = request.POST.get('contact_id')
            contact_to_delete = get_object_or_404(Contact, id=contact_id, user=request.user)
            contact_to_delete.delete()
            messages.success(request, f"Contact '{contact_to_delete.name}' deleted successfully.")
            return redirect('my_contacts')  # update with correct URL name

        return render(request, 'contact/contact.html', {'contacts': contacts})
    
    # For anonymous users, no contacts list
    return render(request, 'contact/contact.html')

 
def dashboard(request):
    if request.user.is_authenticated:
        Totalcontacts = Contact.objects.filter(user=request.user).count()
        TotalCategories = Catagory.objects.filter(user=request.user).count()
        dayContact = Contact.objects.filter(user=request.user, created_at__date=date.today()).count()
        weekContact = Contact.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=7)).count()
        monthContact = Contact.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=30)).count()
        recentAddition=Contact.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=30)).count()

      
        
        recentActivity=Activity.objects.filter(user=request.user).order_by('-activity_date')[:4]  # Get last 5 activities
        

        print(recentActivity)    
        context={
            'Totalcontacts': Totalcontacts,
            'TotalCategories': TotalCategories,
            'dayContact': dayContact,
            'weekContact': weekContact,
            'monthContact': monthContact,
            'recentAddition': recentAddition,
            'recent_activities': recentActivity,
        }
        return render(request, 'contact/dashboard.html',{'context': context})
    return render(request, 'contact/dashboard.html')


def addContact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                contact= form.instance  # Get the saved contact instance
                activity = Activity.objects.create(
                    user=request.user,
                    activity_type='Created',
                    description=f'Contact {contact.name} was added to Your Contact',
                    activity_date=datetime.now()
               )
                return redirect('contact')
        else:
            form= ContactForm(user=request.user)    
        return render(request, 'contact/addContact.html',{'form' : form})
    return render(request, 'contact/addContact.html')

@login_required
def updateContact(request, contact_id):
    contact = Contact.objects.get(id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user, instance=contact)
        if form.is_valid():
            form.save()
            activity = Activity.objects.create(
                    user=request.user,
                    activity_type='Updated',
                    description=f'Contact {contact.name} was Updated',
                    activity_date=datetime.now()
               )
            return redirect('contact')
    else:
        form = ContactForm(instance=contact, user=request.user)
    return render(request, 'contact/updateContact.html', {'form': form, 'contact': contact})


@login_required
def deleteContact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    
    if request.method == 'POST':  # Correct method
      
        activity = Activity.objects.create(
                    user=request.user,
                    activity_type='Deleted',
                    description=f'Contact {contact.name} was Deleted',
                    activity_date=datetime.now()
             )
        contact.delete()
        messages.success(request, f"Contact '{contact.name}' deleted successfully.")

        return redirect('/contact/')  # Use named URL instead of hardcoded path

    # Optional: redirect if not POST
    messages.warning(request, "Invalid request method.")
    return redirect('/contact/')
    