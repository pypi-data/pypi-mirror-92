# Installation

1. `pip install django-mxio-account-management`
2. In `settings.py`, add `account_management` to `INSTALLED_APPS`
3. In `urls.py`, add the url patterns (see section `including URLs` below)
4. Customize `account_management.lib.AccountManagement` (see section `Hacking & customizing`)
5. Customize templates in `templates/account_management` (see section `Hacking & customizing`)
6. You really need to implement `get_default_authenticated_url`, which is where the user gets directed when they log in.


# Including URLs

There are two methods to include URLs:

## Method 1

in urls.py

```
urlpatterns = [
    path('accounts/', include(('account_management.urls', 'account_management), namespace='account_management_custom'))
]
```

This will mount everything using the default paths:

- `/accounts/login/`
- `/accounts/register/`
- `/accounts/set-password/`
- `/accounts/reset-password/`
- `/accounts/logout/`


## Method 2

in urls.py

```
from account_management.urls import get_urlpatterns

acc_urls = get_urlpatterns({
    'login': 'connexion',
    'register': 'enregistrer',
    'set-password': 'definir-mot-de-passe',
    'reset-password': 'reinitialiser-mot-de-passe',
    'logout': 'deconnecter',
})

urlpatterns = [
    path('accounts2/', include((acc_urls, 'account_management'), namespace='account_management_fr'))
]

```

This will mount everything using the paths you defined:

- `/accounts2/connexion/`
- `/accounts2/enregistrer/`
- ...


# Hacking & customizing

So.. I came up with this idea to extend functionality. In `account_management/lib.py` we have a class called `AccountManagement`. Anything that should be customizable (i.e. messages, functions, etc.) should be defined as a default there. Then, if you need to customize, you can subclass `AccountManagement` when using the library and override what you need to.


Let's say this is in `core/lib.py`

```
from account_management.lib import AccountManagement


class AccountManagementCustom(AccountManagement):
  pass
```

Then, add the following to `core/settings.py`:

```
MXIO_ACCOUNT_MANAGEMENT_CLASS = 'core.settings.AccountManagement'
```
