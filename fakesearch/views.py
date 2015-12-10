# Login control
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Django control
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
# FakeSearch classes
from fakesearch.models import ResultList, UserProfile, Experiment, ExperimentSet, Vote, UserExperimentSet
from fakesearch.forms import UserForm, UserProfileForm, VoteForm

#####
#### General screens
#####

def index(request):
    # Render the response and send it back!
    return render(request, 'fakesearch/index.html', {})

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

            set_user_experiment_set(profile)

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


def set_user_experiment_set(user):
    # Gets a random Experient Set
    es = ExperimentSet.objects.order_by('?').first()
    ues = UserExperimentSet.objects.create(user=user, experimentSet=es)
    ues.save()

    # Add votes:
    for e in es.experiments.get_queryset():
        v, created = Vote.objects.get_or_create(user=user, experiment=e)
        v.preference = -1
        v.save()

#####
#### Experiments
#####
@login_required
def experiments(request):
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    experiment_list = []
    experiment_set = None
    ues = UserExperimentSet.objects.get(user=up)

    if ues:
        experiment_set = ues.experimentSet.experiments

    if experiment_set:
        experiments = experiment_set.order_by("pk")
        for experiment in experiments:
            try:
                preference = Vote.objects.get(user=up, experiment=experiment).preference
            except:
                preference = -1
            experiment_list.append((experiment, preference))

    else:
        print "Not Found"

    context_dict = {'experiments': experiment_list}

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'fakesearch/experiments.html', context_dict)

@login_required
def run_experiment(request, exp_pk):

    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    e = get_object_or_404(Experiment, pk=exp_pk)
    v = get_object_or_404(Vote, experiment=e, user=up)

    def getNeighbor(e, up, variation):
        try:
            return UserExperimentSet.objects.get(user=up).experimentSet.experiments.get(pk = e.id + variation)
        except:
            return None
    next_exp = getNeighbor(e, up, +1)
    previous_exp = getNeighbor(e, up, -1)

    context_dict = {'experiment' : e, 'next_exp': next_exp, 'previous_exp': previous_exp, 'vote': v}

    if request.method == 'POST':

        vote_form = VoteForm(data=request.POST, instance=v)
        if vote_form.is_valid():
            vote_instance = vote_form.save()

        if 'next' in request.POST:
            e = next_exp
        if 'previous' in request.POST:
            e = previous_exp
        if 'done' in request.POST:
            return HttpResponseRedirect(reverse('fakesearch:experiments'))
        return HttpResponseRedirect(reverse('fakesearch:run_experiment', args=(e.id,)))

    # it is just the GET method:
    else:
        data_dict = {'preference': v.preference}
        context_dict['vote_form'] = VoteForm(initial=data_dict)

    return render(request, 'fakesearch/run_experiment.html', context_dict)

