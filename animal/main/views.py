from django.shortcuts import render, get_object_or_404, redirect
from .models import AnimalType, Breed, Animal, Weighting
from django.db.models import Q
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import WeightingForm, SignUpForm



def popular_list(request):
    animals = AnimalType.objects.filter(available=True)[:3]
    return render(request, 'main/index/index.html', {'animals': animals})


def product_detail(request, slug):
    animal = get_object_or_404(AnimalType, slug=slug, available = True)
    return render(request, 'main/product/detail.html', {'animal': animal})


def button_page(request):
    return render(request, 'main/templates/animal_list.html')


from datetime import date, timedelta

def animal_list(request):
    animal_types = AnimalType.objects.all()
    breeds = Breed.objects.all()

    selected_type = request.GET.get('type')
    selected_breed = request.GET.get('breed')
    name = request.GET.get('name')
    inventory_number = request.GET.get('inventory_number')
    age_from = request.GET.get('age_from')
    age_to = request.GET.get('age_to')
    arrival_date_from = request.GET.get('arrival_date_from')
    arrival_date_to = request.GET.get('arrival_date_to')

    animals = Animal.objects.all()

    if selected_type:
        animals = animals.filter(breed__animal_type__id=selected_type)

    if selected_breed:
        animals = animals.filter(breed__id=selected_breed)

    if name:
        animals = animals.filter(nickname__icontains=name)

    if inventory_number:
        animals = animals.filter(inventory_number__icontains=inventory_number)

    if age_from:
        age_from_date = date.today() - timedelta(days=int(age_from) * 365.25)
        animals = animals.filter(arrival_date__lte=age_from_date)

    if age_to:
        age_to_date = date.today() - timedelta(days=int(age_to) * 365.25)
        animals = animals.filter(arrival_date__gte=age_to_date)

    if arrival_date_from:
        animals = animals.filter(arrival_date__gte=arrival_date_from)

    if arrival_date_to:
        animals = animals.filter(arrival_date__lte=arrival_date_to)

    return render(request, 'main/animal_list.html', {
        'animals': animals,
        'animal_types': animal_types,
        'breeds': breeds,
        'selected_type': selected_type,
        'selected_breed': selected_breed,
        'name': name,
        'inventory_number': inventory_number,
        'age_from': age_from,
        'age_to': age_to,
        'arrival_date_from': arrival_date_from,
        'arrival_date_to': arrival_date_to,
    })




User = get_user_model()

@login_required
def my_animals(request):
    weightings = Weighting.objects.filter(user=request.user)
    return render(request, 'main/my_animals.html', {'weightings': weightings})

@login_required
def add_weighting(request):
    if request.method == 'POST':
        form = WeightingForm(request.POST)
        if form.is_valid():
            weighting = form.save(commit=False)
            weighting.user = request.user
            weighting.save()
            return redirect('main:my_animals')
    else:
        form = WeightingForm()
    return render(request, 'main/add_weighting.html', {'form': form})

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Пользователь не активен по умолчанию
            user.save()

            # Отправка письма с активацией
            token = user.generate_activation_token()
            mail_subject = 'Activate your account'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            send_mail(mail_subject, message, 'from@example.com', [user.email])
            return redirect('main:registration_complete')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and user.activation_token == token:
        user.is_active = True
        user.activation_token = None
        user.save()
        return redirect('main:activation_complete')
    else:
        return render(request, 'activation_invalid.html')



