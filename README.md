# django-crud-app

this module is extends of *django startapp*

# install

`pip install django-crud-app`

add `crud` to your django settings.py

example)
```python
INSTALLED_APPS = [
    # ...
    'crud',
]
```

# Usage

`python manage.py startcrud <app_name>`

# UserModel

`python manage.py startcrud user`

or

`python manage.py startcrud <app_name> --auth-user True`

# Model name

you can customize created model name

example:

```bash
python manage.py startcrud blog
# model name is 'Blog'

python manage.py startcrud blog --model-name web_blog
# model name is 'WebBlog'
```