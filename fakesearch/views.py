# Login control
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Django control
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
# FakeSearch classes
from fakesearch.models import ResultList, UserProfile, Experiment
from fakesearch.forms import UserForm, UserProfileForm

#####
#### General screens
#####

def index(request):
    context_dict = {}

    # Render the response and send it back!
    return render(request, 'fakesearch/index.html', context_dict)

def about(request):
    return render(request, 'fakesearch/about.html', [])

#####
#### User authentification screens
#####
def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            # Logs in the user now:
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect('/fakesearch/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'fakesearch/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    disable_account = False
    bad_details = False

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/fakesearch/')
            else:
                disable_account = True
                # An inactive account was used - no logging in!
        else:
            bad_details = True
            print "Invalid login details: {0}, {1}".format(username, password)

    return render(request, 'fakesearch/login.html', {'bad_details':bad_details, 'disable_account': disable_account})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/fakesearch/')

def user_profile(request):
    # Render the response and send it back!
    return render(request, 'fakesearch/profile.html', {})

#####
#### Experiments
#####

@login_required
def experiment(request):
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    experiments = Experiment.objects.filter(user=up)
    context_dict = {'experiments': experiments}

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'fakesearch/experiment.html', context_dict)

@login_required
def run_experiment(request, exp_pk):

    # TODO: check if experiment belongs to this user
    # e = Experiment.objects.get(pk = exp_pk)
    e = get_object_or_404(Experiment, pk=exp_pk)
    context_dict = {'experiment' : e}

    if not e:
        print "ERROR HERE!!!!"

    if request.method == 'POST':
        print "Dealing with a POST"
        preference = request.POST.get('preference')
        print preference

        # TODO: check if it is valid. Use a try here
        e.preference = int(preference)
        e.save()
        # TODO: run next experiment as this one we already know what the user decided.
    # it is just the GET method:
    else:
        print "Dealing with a GET"
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
    return render(request, 'fakesearch/run_experiment.html', context_dict)

