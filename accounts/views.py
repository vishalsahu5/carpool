from django.shortcuts import render
from accounts.forms import UserForm, ProfileForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


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
            # UserForm and UserProfileInfoForm
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
