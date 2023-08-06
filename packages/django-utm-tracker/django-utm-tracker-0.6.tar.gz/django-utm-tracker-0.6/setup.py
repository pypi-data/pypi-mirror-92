# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utm_tracker', 'utm_tracker.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-utm-tracker',
    'version': '0.6',
    'description': 'Django app for extracting and storing UTM tracking values.',
    'long_description': '# Django UTM Tracker\n\nDjango app for extracting and storing UTM tracking values.\n\n## Background\n\nThis app has been designed to integrate the standard `utm_*` querystring\nparameters that are used by online advertisers with your Django project.\n\nIt does _not_ replace analytics (e.g. Google Analytics) and Adwords tracking,\nbut does have one crucial difference - it allows you to assign a specific user\nto a campaign advert.\n\nThis may be useful if you are trying to assess the value of multiple channels /\ncampaigns.\n\n## How it works\n\nThe app works as a pair of middleware classes, that extract `utm_` values from\nany incoming request querystring, and then store those parameters against the\nrequest.user (if authenticated), or in the request.session (if not).\n\nThe following shows this workflow (pseudocode - see `test_utm_and_lead_source`\nfor a real example):\n\n```python\nclient = Client()\n# first request stashes values, but does not create a LeadSource as user is anonymous\nclient.get("/?utm_medium=medium&utm_source=source...")\nassert utm_values_in_session\nassert LeadSource.objects.count() == 0\n\n# subsequent request, with authenticated user, extracts values and stores LeadSource\nuser = User.objects.create(username="fred")\nclient.force_login(user, backend=settings.FORCED_AUTH_BACKEND)\nclient.get("/")\nassert not utm_values_in_session\nassert LeadSource.objects.count() == 1\n```\n\n### Why split the middleware in two?\n\nBy splitting the middleware into two classes, we enable the use case where we\ncan track leads without `utm_` querystring parameters. For instance, if you have\nan internal referral program, using a simple token, you can capture this as a\n`LeadSource` by adding sentinel values to the `request.session`:\n\n```python\ndef referral(request, token):\n    # do token handling\n    ...\n    # medium and source are mandatory for lead source capture\n    request.session["utm_medium"] = "referral"\n    request.session["utm_source"] = "internal"\n    # campaign, term and content are optional fields\n    request.session["utm_campaign"] = "july"\n    request.session["utm_term"] = token\n    request.session["utm_content"] = "buy-me"\n    return render(request, "landing_page.html")\n```\n\n## Configuration\n\nAdd the app to `INSTALLED_APPS`:\n\n```\n# settings.py\nINSTALLED_APPS = [\n    ...\n    "utm_tracker"\n]\n```\n\nand add both middleware classes to `MIDDLEWARE`:\n\n```\n# settings.py\nMIDDLEWARE = [\n    ...\n    "utm_tracker.middleware.UtmSessionMiddleware",\n    "utm_tracker.middleware.LeadSourceMiddleware",\n]\n```\n\nThe `UtmSession` middleware must come before `LeadSource` middleware.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-utm-tracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
