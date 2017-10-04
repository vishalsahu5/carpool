from django.shortcuts import render
from accounts.forms import UserForm, ProfileForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and ProfileForm
            profile.user = user

            # Now save model
            profile.save()

            # Registration Successful!
            return HttpResponseRedirect(reverse('accounts:login'))
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = ProfileForm()

    # This is the render and context dictionary to feed
    # back to the signup.html file page.
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'accounts/signup.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            print(profile_form.errors)
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/update_profile.html', {'profile_form': profile_form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {})