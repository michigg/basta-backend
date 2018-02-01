from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from apps.registration.forms import SignUpForm, ChangeUserDataForm
from apps.registration.tokens import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.shortcuts import HttpResponse, redirect
from apps.food.models import UserRating, UserFoodImage


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = request.META['HTTP_HOST']
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.jinja', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            send_mail(from_email="signup.basta@gmail.com", recipient_list=[user.email], subject=subject,
                      message=message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.jinja', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'registration/account_activation_success.jinja')
    else:
        return render(request, 'registration/account_activation_invalid.jinja')


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.jinja', {})


def account_view(request):
    if request.user.is_authenticated:
        user = request.user

        food_ratings = UserRating.objects.filter(user=user).order_by('food__name')
        food_images = UserFoodImage.objects.filter(user=user)
        print(food_images)

        return render(request, 'registration/account_view.jinja',
                      {'name': user.username, 'email': user.email, 'date_joined': user.date_joined,
                       'food_ratings': food_ratings, 'first_name': user.first_name, 'last_name': user.last_name,
                       'last_login': user.last_login, 'food_images': food_images})
    else:
        return HttpResponse(status=404)


def account_change(request):
    if request.user.is_authenticated:
        instance = get_object_or_404(User, id=request.user.id)
        form = ChangeUserDataForm(request.POST, instance=instance, initial={"first_name": "Hallo"})
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('account')
            else:
                return HttpResponse(status=404)
        else:
            return render(request, 'registration/account_data_change.jinja', {'form': form})

    else:
        return HttpResponse(status=404)
