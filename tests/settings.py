#!/usr/bin/env python
HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'django_frontify',
    ],
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }]
    },
    'LANGUAGE_CODE': 'en',
    'ALLOWED_HOSTS': ['*'],
}


def run():
    from app_helper import runner
    runner.run('django_frontify')


if __name__ == '__main__':
    run()
