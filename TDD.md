Technical Development Document
---

# Build/Deploy Step
## Local
### Set variables
```
set -a
source .env
set +a
```
### Build
```    
python3 manage.py makemigrations
python3 manage.py migrate
```
### Run
```
python3 manage.py runserver 0.0.0.0:8000
```
## Local with docker
### Build
```
docker compose build
docker image prune -f
docker scan exam-python
```
- exam-python : Docker image name.
### Run
```
docker compose up -d
```
### Stop
```
docker compose down
```
## Heroku
```
git branch -D herokuStaging
git branch herokuStaging
git push -f heroku herokuStaging:main
```
- herokuStaging : Git branch
## Heroku with docker
### Preparation
```
heroku container:login
```
### Build
```
heroku container:push $IMAGE_NAME
```
### Deploy
```
heroku container:release $IMAGE_NAME
```
---
# Survey 選擇
## URL設定
若使用path來include，則路徑會和plugin的設定相同，
在使用不多的plugin時，直接使用此設定會比較適合，
可以避免plugin的功能異常。
- Sample
```urls.py
urlpatterns = [
    path('', include('Thirds.Party.urls')),
]
```
但plugin的path有重複可能，為了讓多個plugin共同作業，
可透過re_path將plugin的path加上prefix。
- Sample
```urls.py
urlpatterns = [
    re_path(r"^accounts/", include("Thirds.Party.urls")),
    re_path(r"^oauth/", include("Another.Party.urls")),
]
```
## Email Verification
Django的user有個default property: is_active，
原本想使用這個property來當做email是否驗證的判斷，
但是Django在is_active為false時，無法登入，和需求不符，所以只能再額外設定。
## Enviroment Setting
local測試時，可使用下列指令export環境變數
```
set -a
source .env
set +a
```
寫成docker file時，要加上.env。
## Docker image
使用python:3.9-slim-bullseye
```
google 'docker python image best'
```
https://pythonspeed.com/articles/base-image-python-docker-images/
https://dev.to/pmutua/the-best-docker-base-image-for-your-python-application-3o83
## Login Require
https://docs.djangoproject.com/en/4.0/topics/class-based-views/intro/
## Url reverse with pk
```
google 'django view url <int:pk> reverse pk'
```
https://stackoverflow.com/questions/64077828/have-a-django-reverse-to-a-url-with-pk-intpk
## Model的relationship
使用OneToOneField
https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey
# Reference
```
google 'python django local user'
```
https://realpython.com/django-user-management/
- Django model User
- Dashboard View
- Django model User Management
	- login
	- logout
	- change password
- Sign up
- Send email
- Login with github

https://docs.djangoproject.com/en/4.0/topics/auth/customizing/

```
google 'python django USERNAME_FIELD email'
```
https://koenwoortman.com/python-django-email-as-username/
- Django model User

```
google 'bash export file'
```
https://unix.stackexchange.com/questions/79064/how-to-export-variables-from-a-file
# Error Fixing
## Import url error
- Error Message:
```
cannot import name 'url' from 'django.conf.urls'
```
- Solution:
```
from django.urls import re_path
urlpatterns = [
    re_path(r"^dashboard/", dashboard, name="dashboard"),
]
```
- Reference:
https://stackoverflow.com/questions/70319606/importerror-cannot-import-name-url-from-django-conf-urls-after-upgrading-to

## Password template not work
- Solution:
```login/urls.py
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView)
    path('accounts/password_change/',
            PasswordChangeView.as_view(
                template_name=
                "login/templates/registration/password_change_form.html"),
            name='password_change'),
    path('accounts/password_change/done/',
            PasswordChangeDoneView.as_view(
                template_name=
                "login/templates/registration/password_change_done.html"),
            name='password_change_done'),
```
- Reference:
google 'Django Password change template'
https://stackoverflow.com/questions/63861287/django-password-change-template-customization
## Import ugettext error
- Error Message:
```
ImportError: cannot import name 'ugettext' from 'django.utils.translation'
```
- solution
```
from django.utils.translation import gettext_lazy as _
```
- Reference:
 https://stackoverflow.com/questions/71420362/django4-0-importerror-cannot-import-name-ugettext-lazy-from-django-utils-tra
## Import force_text error
- Error Message:
```
ImportError: cannot import name 'force_text' from 'django.utils.encoding' 
```
- solution
```
from django.utils.encoding import force_str
```
- Reference:
https://stackoverflow.com/questions/70382084/import-error-force-text-from-django-utils-encoding
# 未使用的Survey
## Change password template
於as_view的參數增加`success_url`，可控制redirect的page。
- Sample
```login/urls.py
    path('accounts/password_change/',
         PasswordChangeView.as_view(
             template_name="login/templates/registration/password_change_form.html",
			 success_url='/',),
         name='password_change'),
```
### Reference
https://techpluslifestyle.com/technology/django-reset-password/

## PasswordResetTokenGenerator
https://forum.djangoproject.com/t/django-passwordresettokengenerator/5872