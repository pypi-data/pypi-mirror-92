# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solvent']

package_data = \
{'': ['*'],
 'solvent': ['sites/action.greene2020.com/stop-the-steal-rd/*',
             'sites/action.iowagunowners.org/action/re-open-iowa-for-business/*',
             'sites/action.iowagunowners.org/sign-up/*',
             'sites/defendyourballot.formstack.com/forms/voter_fraud/*',
             'sites/donjr.com/@/*',
             'sites/donjr.com/challenge/*',
             'sites/donjr.com/collections/all/default.yml',
             'sites/donjr.com/collections/all/products/{slug}/*',
             'sites/donjr.com/{product}/checkouts/{cart}/*',
             'sites/iqconnect.lmhostediq.com/iqextranet/EsurveyForm.aspx/*',
             'sites/nolabels.salsalabs.org/071020trumphandlingcovid--19/index.html/*',
             'sites/oneclickpolitics.global.ssl.fastly.net/messages/edit/*',
             'sites/rebellegends.org/@/*',
             'sites/reopennc.com/@/*',
             'sites/secure.anedot.com/greene-for-congress-inc/stop-the-steal-rd/*',
             'sites/secure.donaldjtrump.com/official-2020-strategy-survey/*',
             'sites/shop.donaldjtrump.com/@/*',
             'sites/steube.house.gov/@/*',
             'sites/steube.house.gov/contact/newsletter/*',
             'sites/steube.house.gov/contact/newsletter/newsletter-subscribe-thank-you/*',
             'sites/trumpvictory.com/free-yard-sign/*',
             'sites/unlockmichigan.com/thank-you/*',
             'sites/unlockmichigan.ivolunteers.com/Account/Register/*',
             'sites/unlockmichigan.ivolunteers.com/Account/ThankYou/*',
             'sites/unlockmichigan.ivolunteers.com/Error/NotFound/*',
             'sites/unlockmichigan.ivolunteers.com/Register/extrapetitions/*',
             'sites/www.beckysflowersmidland.com/contacts.html/*',
             'sites/www.beckysflowersmidland.com/index.html/*',
             'sites/www.donaldjtrump.com/@/*',
             'sites/www.donaldjtrump.com/landing/the-official-2020-strategy-survey/*',
             'sites/www.facebook.com/login.php/*',
             'sites/www.mypillow.com/@/*',
             'sites/www.paypal.com/checkoutnow/*']}

install_requires = \
['pomace>=0.6.8,<0.7.0']

extras_require = \
{':sys_platform == "darwin"': ['caffeine>=0.5,<0.6']}

entry_points = \
{'console_scripts': ['solvent = solvent:main']}

setup_kwargs = {
    'name': 'solvent',
    'version': '20.1.16',
    'description': 'Kills off fake grass.',
    'long_description': None,
    'author': 'Solvent',
    'author_email': 'solvent@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
