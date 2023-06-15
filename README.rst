===============
django Frontify
===============

Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/lab360-ch/django-frontify/blob/master/setup.py>`_
file for additional dependencies:

Installation
------------

 * run ``pip install django-frontify``
 * add ``django_frontify`` to your ``INSTALLED_APPS``
 * add configuration (as mentioned below) to your settings file


Configuration
-------------

* Set ``DJANGO_FRONTIFY_DOMAIN="<your-frontify-donmain>"`` in your settings.py
* Set ``DJANGO_FRONTIFY_FINDER_VERSION=2`` in your settings.py
* Set ``DJANGO_FRONTIFY_CLIENT_ID="<your-client-id>"`` in your settings.py


Version usage
-------------
Frontify has released a new version of its Finder, which made the previous version (v1) a legacy version.
To still use the legacy version, set ``DJANGO_FRONTIFY_FINDER_VERSION=1``.
Otherwise, beware that you've set ``DJANGO_FRONTIFY_CLIENT_ID="<your-client-id>"``


Tecnical questions about frontify?
----------------------------------

Frontify Slack Channel:  
https://frontify-friends.slack.com/join/shared_invite/zt-b910hbol-9cGnIaCet11a9D4uzpVWmQ#/shared-invite/email 

Frontify API Documentation:  
https://developer.frontify.com/ 


Development
=============

Localsetup
------------

Run this command in one terminal

    make runserver

and this in a other

    make watch_static

now you should be able to accesses the example django project via http://localhost:8000


Release requirements
--------------------

to release a package you have to add the following file

    vim ~/.pypirc

with the following content

.. code-block::DJANGO_FRONTIFY_CLIENT_ID

    [distutils]
    index-servers =
      pypi
      pypitest
    
    [pypi]
    repository: https://pypi.python.org/pypi
    username: YOUR_USERNAME_HERE
    password: YOUR_PASSWORD_HERE
    
    [pypitest]
    repository: https://test.pypi.org/legacy/
    username: YOUR_USERNAME_HERE
    password: YOUR_PASSWORD_HERE


Release package
---------------

First do a test release with this command:

    make test_release

then run this for the real release:

    make release

