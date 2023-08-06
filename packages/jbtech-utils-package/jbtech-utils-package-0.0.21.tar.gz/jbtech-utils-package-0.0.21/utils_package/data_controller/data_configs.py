""" Get configs for data controller related applications """
from utils_package.api_controller.configman import ConfigmanController
from utils_package.py_utils import primary_utils

UTIL_VARS = ConfigmanController().get_application_configs('jb_tech_utils', 'vars')


class DataConfigs:
    """ Handling the data retrieval for an application """

    def __init__(self):
        """ Initialize class variables """
        self.env = primary_utils.get_current_env()

    def get_db_dict(self, user):
        """
        Method to build the proper database dictionary to generate a connection
        :param user: User that will be running the SQL command
        :return: Dictionary of the user and connection information
        """
        db_dict = {'host': UTIL_VARS['postgres.%s.server' % self.env],
                   'port': UTIL_VARS['postgres.%s.port' % self.env],
                   'dbname': UTIL_VARS['postgres.%s.db_name' % self.env],
                   'username': user,
                   'password': UTIL_VARS['postgres.%s.cred.%s' % (self.env, user)]}
        return db_dict
