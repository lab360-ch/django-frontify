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
 * add ``django-frontify`` to your ``INSTALLED_APPS``
 * add ``DJANGO_FRONTIFY_DOMAIN`` to your settings file


Configuration
-------------

Set ``DJANGO_FRONTIFY_DOMAIN="<your-frontify-donmain>"`` in your settings.py


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

.. code-block::

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

