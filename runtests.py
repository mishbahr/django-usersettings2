import sys

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        ROOT_URLCONF='example.urls',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'django.contrib.messages',
            'usersettings',
            'example',
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        USERSETTINGS_MODEL='example.SiteSettings',
        MIDDLEWARE_CLASSES=(
            'usersettings.middleware.CurrentUserSettingsMiddleware',
        ),
        TEMPLATE_CONTEXT_PROCESSORS = (
            'django.core.context_processors.request',
            'usersettings.context_processors.usersettings',
        )
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

    from django_nose import NoseTestSuiteRunner
except ImportError as e:
    print e
    raise ImportError('To fix this error, run: pip install -r requirements-test.txt')


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
