from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
import json
import requests

from django.contrib.auth.forms import PasswordChangeForm

def index(request):
    user = request.user

    if not user.is_authenticated:
        return render(request, 'index.html')

    auth0user = user.social_auth.get(provider='auth0')
    if not auth0user.extra_data['email_verified']:
        return render(request, 'email_verification.html')

    return redirect(dashboard)
        

@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
        'email_verified': auth0user.extra_data['email_verified'],
    }

    return render(request, 'dashboard.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })

@login_required
def resend_verification_email(request):
    user = request.user
    auth0_user = user.social_auth.get(provider='auth0')
    
    # Get an Access Token from Auth0
    base_url = f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}"
    payload =  { 
        'grant_type': 'client_credentials',
        'client_id': settings.SOCIAL_AUTH_AUTH0_API_KEY,
        'client_secret': settings.SOCIAL_AUTH_AUTH0_API_SECRET,
        'audience': f'{base_url}/api/v2/'
    }
    response = requests.post(f'{base_url}/oauth/token', data=payload)
    oauth = response.json()
    access_token = oauth.get('access_token')
    print(response.json())

    # Email Verification
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }    
    user_data = {
        'user_id': auth0_user.uid,
        'client_id':settings.SOCIAL_AUTH_AUTH0_KEY,
        'identity': {
            'provider': 'auth0',
            'user_id' : _get_identity_user_id(auth0_user.uid, 'auth0'),
        }
    }

    url = f'{base_url}/api/v2/jobs/verification-email'
    response = requests.post(url,headers=headers,data = json.dumps(user_data))
    print(response.json())
    return render(request, 'email_verification.html')


def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.clean_new_password2()

            user = request.user
            auth0_user = user.social_auth.get(provider='auth0')
            uid = auth0_user.uid

            _reset_password(uid, new_password)

            return render(request, 'dashboard.html')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'reset_password.html', {'form': form})


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)

def _get_identity_user_id(user_id, provider):
    prefix = provider + '|'
    if user_id.startswith(prefix):
        return user_id[len(prefix):]
    return user_id


def _reset_password(uid, new_password):
    headers = {
        'Content-Type': 'application/json'
    }    
    payload = {
        "email_verified": false,
        'password': new_password,
        'connection':'Initial-Connection',
    }
    url = f'{base_url}/api/v2/users/{uid}'
    response = requests.patch(url,headers=headers,data = json.dumps(user_data))
    print(response.json())
