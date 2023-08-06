""" Controller for handing the configman requests """
from utils_package.data_controller.json_config import JSONConfig
from utils_package.py_utils.logger import logger
import requests
import json


class ConfigmanController:
    """ Handling the API calls for configman """

    def __init__(self):
        """ Initialize class variables """
        self.json_config = JSONConfig()
        self.urls = JSONConfig().get_configman_config('urls')
        self.base_url = JSONConfig().get_configman_config('base_url')

    def generate_auth_token(self, password, user, app):
        """ Generate an auth token using the application password sent
        1. Build request
        2. Send request
        3. Generate response
        4. Return content as dict and status cod
        :param password: Password for the application cred
        :param user: User for the application cred
        :param app: Application to which the user cred belongs
        :return: status_code, content
        """
        # 1. Build request
        request = {
            'user': user,
            'password': password,
            'app': app
        }
        request_url = self.base_url + self.urls['generate_token']

        # 2. Send request
        logger.info('Sending API request for configman token generation')
        logger.info('Request URL: %s' % request_url)
        logger.info('User: %s' % user)
        response = requests.post(request_url, json=request)

        # 3. Generate response
        content = json.loads(response.content)
        status_code = response.status_code

        # 4. Return content and status code
        return status_code, content

    def validate_auth_token(self, token, user):
        """ Validate the authentication token
        1. Build request
        2. Send request
        3. Generate response
        4. Return response
        :param token: Token to be evaluated
        :param user: User the token should belong to
        :return: status_code, content
        """
        # 1. Build request
        request = {
            'user': user,
            'token': token
        }
        request = json.dumps(request)
        request_url = self.base_url + self.urls['validate_token']

        # 2. Send request
        logger.info('Sending API request for configman token validation')
        logger.info('Request URL: %s' % request_url)
        logger.info('User: %s' % user)
        response = requests.post(request_url, json=request)

        # 3. Generate response
        content = json.loads(response.content)
        status_code = response.status_code

        # 4. Return response
        return status_code, content

    def load_application_configs(self, token, user, app, config_type):
        """ Returns all application configs in order to load them into memory
        1. Build request
        2. Send request
        3. Generate response
        4. Return response
        :param token: Token for the user
        :param user: User for the application
        :param app: Application to get configs
        :param config_type: Type of configs to be returned
        :return: All configurations for the given application
        """
        # 1. Build request
        request = {
            'configType': config_type,
            'app': app
        }
        headers = {
            'user': user,
            'Authorization': token
        }
        request_url = self.base_url + self.urls['get_configs']

        # 2. Send request
        logger.info('Sending API request for configman configuration retrieval')
        logger.info('Request URL: %s' % request_url)
        logger.info('User: %s' % user)
        response = requests.request('POST', request_url, json=request, headers=headers)

        # 3. Generate response
        content = json.loads(response.content)
        status_code = response.status_code

        # 4. Return response
        return status_code, content

    def get_application_configs(self, application, config_type):
        """
        Method to get the application credentials
        :param application: Application to get the configman configs from
        :param config_type: Type of configuration
        :return: Fill dict of configman for the given config type
        """
        if application not in ['jb_tech_utils', 'email_controller', 'resume_site']:
            raise ValueError('Invalid Application Type: %s' % application)
        if config_type not in ['dirs', 'vars']:
            raise ValueError('Invalid Configuration Type: %s' % config_type)
        app_creds = self.json_config.get_app_credentials(application)
        status_code, response = self.generate_auth_token(app_creds['pass'], app_creds['user'], application)
        if status_code != 202:
            raise ValueError('Invalid Configman Response | Token Generation: %s | %s' % (str(status_code), response))
        token = response['response']['token']
        status_code, response = self.load_application_configs(token, app_creds['user'], application, config_type)
        if status_code != 200:
            raise ValueError('Invalid Configman Response | Load App Configs: %s | %s' % (str(status_code), response))
        return response['response']
