# cases/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CriminalCase, Criminal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from django.views import View


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def home(request):
    cases = CriminalCase.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'cases': cases})


@login_required(login_url='user_login')
def add_criminal_case(request):
    if request.method == 'POST':
        case_number = request.POST.get('case_number')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dob = request.POST.get('dob')
        description = request.POST.get('description')
        reported_by = request.user
        location = request.POST.get('location')

        # Create Criminal
        criminal = Criminal.objects.create(
            firstname=firstname,
            lastname=lastname,
            dob=dob

        )

        # Create Criminal Case
        criminal_case = CriminalCase.objects.create(
            case_number=case_number,
            individual=criminal,
            description=description,
            reported_by=reported_by,
            location=location
            # Add more fields as needed
        )

        return redirect('home')

    return render(request, 'add_criminal_case.html')


def criminal_cases(request):
    criminal_cases = CriminalCase.objects.all()
    return render(request, 'criminal_cases.html', {'criminal_cases': criminal_cases})


class CriminalDetailView(View):
    template_name = 'criminal_detail.html'

    def get(self, request, case_number, *args, **kwargs):
        criminal_case = get_object_or_404(
            CriminalCase, case_number=case_number)
        return render(request, self.template_name, {'criminal_case': criminal_case})
