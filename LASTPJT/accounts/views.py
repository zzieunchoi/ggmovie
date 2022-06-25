from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm, ProfileForm
from community.models import Community
from .models import Profile

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:home')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        id = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=id, password=pwd)
        if form.is_valid():
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'movies:home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:home')


@login_required
def profile(request, user_pk):
    person = get_object_or_404(get_user_model(), pk = user_pk)
    profiles = person.profile.all()
    profile = ''
#    like = Community.objects.filter(username = username)
    for p in profiles:
        profile = p

    context = {
        'person': person,
        'profile':profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def profile_create(request, user_pk):
    person = get_object_or_404(get_user_model(), pk= user_pk)
    if request.user == person:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('accounts:profile', user_pk)
        else:
            form = ProfileForm()
        context = {
            'form': form,
            'person':person,
        }
        return render(request, 'accounts/profile_create.html', context)
    else:
        return redirect('accounts:profile', user_pk)


@login_required
@require_http_methods(['GET','POST'])
def profile_update(request, user_pk, profile_pk):   
    person = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user == person:
        profile = Profile.objects.get(pk=profile_pk)
        if profile == None:
            return redirect('accounts:profile_create', user_pk)
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('accounts:profile', user_pk)
        else:
            form = ProfileForm(instance=profile)
        context = {
            'form' : form,
            'profile' : profile,
        }
        return render(request, 'accounts/profile_update.html', context)
    else:
        return redirect('accounts:profile', user_pk)

@require_POST
def profile_delete(request, user_pk, profile_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        profile = Profile.objects.get(pk=profile_pk)
        if person == user:
            profile.delete()
            return redirect('accounts:profile', user_pk)
        else:
            return redirect('accounts:profile', user_pk)

@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                follow = False
            else:
                person.followers.add(user)
                follow = True
            context = {
                'follow':follow,
                'followers_count' : len(person.followers.all()),
                'followings_count' : len(person.followings.all()),
                }
            return JsonResponse(context)
