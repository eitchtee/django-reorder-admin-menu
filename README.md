# django-reorder-admin-menu

This is a simple snippet of code for reordering your django admin-menu leveraging and rewriting Django Admin's `get_app_list` function.

## Usage

1. Copy the code from [`django-reorder-admin-menu.py`](https://github.com/eitchtee/django-reorder-admin-menu/blob/main/django-reorder-admin-menu.py) and place it on the end of your `settings.py` as below:
```python
def get_app_list(self, request, app_label=None):
  [copied code]
      
# Covering django.contrib.admin.AdminSite.get_app_list
from django.contrib import admin

admin.AdminSite.get_app_list = get_app_list
```
2. Just above this, create a list called `ADMIN_ORDERING`, this is where you will configure the ordering and menus for your Django Admin
```python
ADMIN_ORDERING = []
```

### Configuring

`ADMIN_ORDERING` is a list of dicts, each dict must contain an `app` definition, and optionally a `label` and `models` definition

- `app` is the name of the main django app this entry is defining
- `label` is the name you want the menu entry to have, if not provided the `app`'s verbose_name will be used
- `models` is the, ordered, list of models you want this menu to have, if not provided, all registered models from the `app` will be added

For convenience, two general operators are supported:
- `*` if you want to add all registered models from the `app` to the menu
- `%` if you want to add all registered models that haven't been added in other menu entries yet

#### Caveats and Nuances

- Any model added that isn't registered will be ignored
- For now, to avoid extra loops, the `%` operator doesn't look ahead, so if you add it before declaring all the app's models you want, it will duplicate your entries. Use it only after declaring all models
- Breadcrumbs aren't altered, but they are supported: if you click a breadcrumb for an app you didn't define in `ADMIN_ORDERING`, it will still work, displaying all models for that app.

# Cross-app reference

You can add models from other apps using dot notation.

For example, if you have an `accounts` app with an `User` model and want to add it to the `auth` menu, you can do as follows:

```python
ADMIN_ORDERING = [
    {"app": "auth", "models": ["Group", "accounts.User"]}
]
```

## Example

```python
ADMIN_ORDERING = [
    {"app": "auth", "models": ["Group", "accounts.User"]},
    {"app": "app1", "label": "My custom label", "models": ["*"]},
    {
        "app": "app2",
        "models": ["Model1", "Model2"],
    },
    {
        "app": "app2",
        "label": "app2:fun_stuff",
        "models": [
            "Model3",
            "Model4",
            "Model5",
            "Model6",
        ],
    },
    {
        "app": "app2",
        "label": "app2 - other stuff",
        "models": ["%"],
    },
]
```

Will result in something like this

![image](https://github.com/eitchtee/django-reorder-admin-menu/assets/10510126/296a4aed-5f89-4c94-af0c-4f99e24d90dd)


## Attribution

This code is heavily based on [mishbahr's django-modeladmin-reorder](https://github.com/mishbahr/django-modeladmin-reorder) and on a plethora of StackOverflow's answers whose references have been lost in the mess that was coding this.

_If you believe your code is in any way refereced here, please open an issue or PR._
