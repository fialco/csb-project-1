# csb-project-1

[Project 1](https://cybersecuritybase.mooc.fi/module-3.1) for Cyber Security Base course by University of Helsinki and MOOC.fi

## Installation

1. Download the project
2. Go to project directory
3. Additionally with other packages installed in [installation-guide](https://cybersecuritybase.mooc.fi/installation-guide), the app uses [django-ratelimit](https://pypi.org/project/django-ratelimit/) for flaw 4 fix. Install package with:

```
python3 -m pip install django-ratelimit
```

4. Initialize database with:

```
python manage.py migrate
```

## Usage

1. Start the app with:

```
python manage.py runserver
```

2. Access the app with a browser by going to [http://localhost:8000](http://localhost:8000)

3. For testing, migration automatically creates users with accounts.
Use [these](https://github.com/fialco/csb-project-1/blob/main/phoneypay/migrations/0002_auto_20260115_1650.py#L16) accounts to log in (for example username: user1, password: password1)
