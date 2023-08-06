# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reddit_get', 'reddit_get.types']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0',
 'praw>=7.1.0,<8.0.0',
 'titlecase>=2.0.0,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['reddit-get = reddit_get.cli:main']}

setup_kwargs = {
    'name': 'reddit-get',
    'version': '1.0.0',
    'description': 'A CLI to get reddit content',
    'long_description': '# Reddit Get\n\nThis is a python CLI that will pull posts from Reddit. In order to use this CLI, you\'ll need to set up a \nReddit app of your own so that you can authenticate into Reddit with your own credentials. Never fear, \nthis process is pretty straight forward.\n\n## Installation\n\nUsing python 3.8 or later, run `pip3 install reddit-get`. But also, you need to set up a reddit cli app so \nyou can access reddit through the command line. See below for that.\n\n### Create a Reddit Application\n\n1. Navigate to https://reddit.com/prefs/apps\n1. Click `create an app`\n1. You should see something like this:\n\n    ![create an app form](assets/create_an_app_form.png)\n\n1. You can then fill this form out with some values like these (choose whatever you like):\n\n    ![create an app form filled](assets/create_an_app_form_filled.png)\n\nAfter that, you\'ll need to find the `client_id` and `client_secret` for your new app and insert those into \na configuration file on your system.\n\n### Adding a Reddit-Get Config File\n\n1. Create a file in your home directory called `.redditgetrc` (currently this is the default name and is \n   only configurable when you call the script each time, so this name is probably for the best for now)\n1. Make your reddit config file look like this:\n\n    ```toml\n   [reddit-get]\n   client_id = "<your client id here>"\n   client_secret = "<your client secret here>"\n   user_agent = "<anything, e.g. My super awesome cli app by u/pm_me_myour_apps>" \n   username = "<your reddit username>"\n   password = "<your reddit password>"\n   ```\n\nOnce this is set up, you should be good to go. \n\n## Example Usage\n\nOnce you\'ve got your cli app set up and reddit-get installed, you can run it like this:\n\n```shell\n$ reddit-get post --subreddit showerthoughts --post_sorting top --limit 10 --time_filter all --header --markdown\n```\nAnd here\'s what was returned today:\n\n```markdown\n##### *Top Posts from r/showerthoughts*\n- *Whoever created the tradition of not seeing the bride in the wedding dress beforehand saved countless husbands everywhere from hours of dress shopping and will forever be a hero to all men.*\n- *We laugh at dogs getting excited when they hear a bark on TV, but if TV was a nonstop stream of unintelligible noises and then someone suddenly spoke to you in your language, you\'d be pretty fucking startled too.*\n- *When you\'re a kid, you don\'t realize you\'re also watching your mom and dad grow up.*\n- *Dads probably bond with dogs so much because, in our society, men don’t get shown a lot of affection but dogs give tons of affection regardless*\n- *Being able to tolerate the sound of your own voice in a video is probably the highest form of self acceptance.*\n- *Girls don\'t compliment guys because they\'re likely to take it non-platonically, guys take it non-platonically because it happens so infrequently they don\'t know how to handle it*\n- *If elevators hadn\'t been invented, all the CEOs and important people would have their offices on the first floor as a sign of status.*\n- *If EA suffers big enough losses from the backlash of Battlefront 2, and it all started because some guy couldn\'t unlock Vader, this will be the second time Anakin brought balance to something.*\n- *Being able to do well in high school without having to put in much effort is actually a big disadvantage later in life.*\n- *During a nuclear explosion, there is a certain distance of the radius where all the frozen supermarket pizzas are cooked to perfection.*\n```\n\nFor more help with the post command, you can of course run\n\n```shell\n$ reddit-get post --help\n```\n\n---\n\nEnjoy! This is early stages, so I\'ll be adding more features as time goes on.\n',
    'author': 'Michael Lane',
    'author_email': 'mikelane@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mikelane/reddit-get',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
