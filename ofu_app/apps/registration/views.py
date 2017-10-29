from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from apps.registration.forms import SignUpForm
from apps.registration.tokens import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.shortcuts import HttpResponse


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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            res = send_mail(
                'Subject here',
                'Here is the message.',
                'signup.basta@gmail.com',
                ['mgoetz1995@gmail.com'],
                fail_silently=False,
            )
            # res = send_mail(from_email="signup.basta@gmail.com", recipient_list=[user.username], subject=subject, message=message)
            return HttpResponse('%s' % res)
            # user.email_user(subject, message)
            # return redirect('account_activation_sent')
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
    return render(request, 'home.jinja', {})
