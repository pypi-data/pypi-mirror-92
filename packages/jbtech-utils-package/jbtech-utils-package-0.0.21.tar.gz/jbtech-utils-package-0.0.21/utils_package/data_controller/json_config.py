""" Postgres Configuration """
from utils_package.py_utils import primary_utils


class JSONConfig:
    """ All methods for postgres configuration """

    def __init__(self):
        """ Set up class variables """
        self.env = primary_utils.get_current_env()
        self.utils = primary_utils

    def get_configman_config(self, config_library):
        """
        Method to get the configman configurations
        :param config_library: Configuration library
        :return: Configuration library return for given param
        """
        controller_dict = self.__read_config_file('systems_config.json')['configman']
        if config_library == 'base_url':
            controller_dict = controller_dict[config_library][self.env]
        else:
            controller_dict = controller_dict[config_library]
        return controller_dict

    def get_app_credentials(self, application):
        """
        Method to pull the application credentials
        :param application: Application for the needed credentials
        :return: Username and Password of the application to be set up
        """
        app_dict = self.utils.open_config_file('application_credentials.json')
        return app_dict[self.env][application]

    def __read_config_file(self, file_name):
        """
        Method to read the default config file for the postgres database
        :return: Dictionary of the config file
        """
        response = self.utils.open_config_file(file_name)
        return response
