"""
Browser set up for acceptance tests.
"""

#pylint: disable=E1101
#pylint: disable=W0613

from lettuce import before, after, world
from splinter.browser import Browser
from logging import getLogger
from django.core.management import call_command
from django.conf import settings
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from base64 import encodestring
from json import dumps

from pymongo import MongoClient
import xmodule.modulestore.django
from xmodule.contentstore.django import _CONTENTSTORE

# There is an import issue when using django-staticfiles with lettuce
# Lettuce assumes that we are using django.contrib.staticfiles,
# but the rest of the app assumes we are using django-staticfiles
# (in particular, django-pipeline and our mako implementation)
# To resolve this, we check whether staticfiles is installed,
# then redirect imports for django.contrib.staticfiles
# to use staticfiles.
try:
    import staticfiles
    import staticfiles.handlers
except ImportError:
    pass
else:
    import sys
    sys.modules['django.contrib.staticfiles'] = staticfiles
    sys.modules['django.contrib.staticfiles.handlers'] = staticfiles.handlers

LOGGER = getLogger(__name__)
LOGGER.info("Loading the lettuce acceptance testing terrain file...")

MAX_VALID_BROWSER_ATTEMPTS = 20


def get_saucelabs_username_and_key():
    """
    Returns the Sauce Labs username and access ID as set by environment variables
    """
    return {"username": settings.SAUCE.get('USERNAME'), "access-key": settings.SAUCE.get('ACCESS_ID')}


def set_saucelabs_job_status(jobid, passed=True):
    """
    Sets the job status on sauce labs
    """
    config = get_saucelabs_username_and_key()
    url = 'http://saucelabs.com/rest/v1/{}/jobs/{}'.format(config['username'], world.jobid)
    body_content = dumps({"passed": passed})
    base64string = encodestring('{}:{}'.format(config['username'], config['access-key']))[:-1]
    headers = {"Authorization": "Basic {}".format(base64string)}
    result = requests.put(url, data=body_content, headers=headers)
    return result.status_code == 200


def make_saucelabs_desired_capabilities():
    """
    Returns a DesiredCapabilities object corresponding to the environment sauce parameters
    """
    desired_capabilities = settings.SAUCE.get('BROWSER', DesiredCapabilities.CHROME)
    desired_capabilities['platform'] = settings.SAUCE.get('PLATFORM')
    desired_capabilities['version'] = settings.SAUCE.get('VERSION')
    desired_capabilities['device-type'] = settings.SAUCE.get('DEVICE')
    desired_capabilities['name'] = settings.SAUCE.get('SESSION')
    desired_capabilities['build'] = settings.SAUCE.get('BUILD')
    desired_capabilities['video-upload-on-pass'] = False
    desired_capabilities['sauce-advisor'] = False
    desired_capabilities['capture-html'] = True
    desired_capabilities['record-screenshots'] = True
    desired_capabilities['selenium-version'] = "2.34.0"
    desired_capabilities['max-duration'] = 3600
    desired_capabilities['public'] = 'public restricted'
    return desired_capabilities


@before.harvest
def initial_setup(server):
    """
    Launch the browser once before executing the tests.
    """
    world.absorb(settings.LETTUCE_SELENIUM_CLIENT, 'LETTUCE_SELENIUM_CLIENT')

    if world.LETTUCE_SELENIUM_CLIENT == 'local':
        browser_driver = getattr(settings, 'LETTUCE_BROWSER', 'chrome')

        # There is an issue with ChromeDriver2 r195627 on Ubuntu
        # in which we sometimes get an invalid browser session.
        # This is a work-around to ensure that we get a valid session.
        success = False
        num_attempts = 0
        while (not success) and num_attempts < MAX_VALID_BROWSER_ATTEMPTS:
            world.browser = Browser(browser_driver)
            world.browser.driver.set_script_timeout(10)

            # Try to visit the main page
            # If the browser session is invalid, this will
            # raise a WebDriverException
            try:
                world.visit('/')

            except WebDriverException:
                world.browser.quit()
                num_attempts += 1

            else:
                success = True

        # If we were unable to get a valid session within the limit of attempts,
        # then we cannot run the tests.
        if not success:
            raise IOError("Could not acquire valid {driver} browser session.".format(driver=browser_driver))

        world.absorb(0, 'IMPLICIT_WAIT')
        world.browser.driver.set_window_size(1280, 1024)

    elif world.LETTUCE_SELENIUM_CLIENT == 'saucelabs':
        config = get_saucelabs_username_and_key()
        world.browser = Browser(
            'remote',
            url="http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(config['username'], config['access-key']),
            **make_saucelabs_desired_capabilities()
        )
        world.absorb(30, 'IMPLICIT_WAIT')
        world.browser.set_script_timeout(10)

    elif world.LETTUCE_SELENIUM_CLIENT == 'grid':
        world.browser = Browser(
            'remote',
            url=settings.SELENIUM_GRID.get('URL'),
            browser=settings.SELENIUM_GRID.get('BROWSER'),
        )
        world.absorb(30, 'IMPLICIT_WAIT')
        world.browser.driver.set_script_timeout(10)

    else:
        raise Exception("Unknown selenium client '{}'".format(world.LETTUCE_SELENIUM_CLIENT))

    world.browser.driver.implicitly_wait(world.IMPLICIT_WAIT)
    world.absorb(world.browser.driver.session_id, 'jobid')


@before.each_scenario
def reset_data(scenario):
    """
    Clean out the django test database defined in the
    envs/acceptance.py file: mitx_all/db/test_mitx.db
    """
    LOGGER.debug("Flushing the test database...")
    call_command('flush', interactive=False, verbosity=0)
    world.absorb({}, 'scenario_dict')


@after.each_scenario
def clear_data(scenario):
    world.spew('scenario_dict')


@after.each_scenario
def reset_databases(scenario):
    '''
    After each scenario, all databases are cleared/dropped.  Contentstore data are stored in unique databases
    whereas modulestore data is in unique collection names.  This data is created implicitly during the scenarios.
    If no data is created during the test, these lines equivilently do nothing.
    '''
    mongo = MongoClient()
    mongo.drop_database(settings.CONTENTSTORE['OPTIONS']['db'])
    _CONTENTSTORE.clear()

    modulestore = xmodule.modulestore.django.editable_modulestore()
    modulestore.collection.drop()
    xmodule.modulestore.django.clear_existing_modulestores()


@after.each_scenario
def screenshot_on_error(scenario):
    """
    Save a screenshot to help with debugging.
    """
    if scenario.failed:
        try:
            output_dir = '{}/log'.format(settings.TEST_ROOT)
            image_name = '{}/{}.png'.format(output_dir, scenario.name.replace(' ', '_'))
            world.browser.driver.save_screenshot(image_name)
        except WebDriverException:
            LOGGER.error('Could not capture a screenshot')

@after.all
def teardown_browser(total):
    """
    Quit the browser after executing the tests.
    """
    if world.LETTUCE_SELENIUM_CLIENT == 'saucelabs':
        set_saucelabs_job_status(world.jobid, total.scenarios_ran == total.scenarios_passed)
    world.browser.quit()
