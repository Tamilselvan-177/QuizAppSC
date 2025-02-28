from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is verified
            user.save()
            
            # Generate correct UID and token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            print(f"UID: {uid}, Token: {token}")  # Debugging output

            # Ensure correct URL pattern
            try:
                verification_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
                activation_url = f"http://{get_current_site(request).domain}{verification_link}"
            except Exception as e:
                print(f"Reverse URL Error: {e}")

            # Send email
            message = render_to_string('email_verification.html', {
                'user': user,
                'activation_url': activation_url,
            })
            send_mail(
                subject='Activate your account',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            messages.success(request, "Signup successful! Please check your email to verify your account.")
            return redirect('signin')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been verified! You can now log in.")
        return redirect('signin')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('signup')

def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the input is a valid username or email
        try:
            user = User.objects.get(email=username_or_email)
            username = user.username
        except User.DoesNotExist:
            username = username_or_email
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You have successfully logged in.")  
                return redirect('dashboard')
            else:
                messages.error(request, "Your account is not verified. Please check your email for the activation link.")
        else:
            messages.error(request, "Invalid username or email, and/or password.")
    
    return render(request, 'signin.html')

@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'dashboard.html')
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('signin')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from .forms import ForgotPasswordForm, ResetPasswordForms

def forgot_password(request):
    """Handles forgot password functionality."""
    form = ForgotPasswordForm()
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                domain = request.get_host()

                # Email content
                subject = "Reset Your Password"
                message = render_to_string('reset_password_email.html', {
                    'domain': domain,
                    'token': token,
                    'uid': uid,
                })

                send_mail(subject, message, 'noreply@example.com', [email])
                return render(request, "reset_password_sent.html")  # Redirect to confirmation page

            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')

    return render(request, "forgot_password.html", {"form": form})


def reset_password(request, uidb64, token):
    """Handles password reset functionality."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = ResetPasswordForms(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('signin')
            else:
                messages.error(request, "Invalid form submission.")
        else:
            form = ResetPasswordForms()
    else:
        messages.error(request, "The password reset link is invalid or expired.")
        return redirect('forgot_password')

    return render(request, 'reset_password.html', {"form": form})
