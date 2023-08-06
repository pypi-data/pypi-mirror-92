""" Queries for hitting the catcha cookie table """
from utils_package.data_controller.pg_util import PGUtil
from utils_package.data_controller import query_tools


class SiteCaptchaResultsWriter(object):
    """ Queries for writing to the coreapp schema on the site captcha results table """

    def __init__(self):
        """ Set up class variables """
        self.captcha_pg = PGUtil(user='app_writer')

    def insert_new_record(self, rel_dict):
        """
        Inserts a new record to coreapp.site_captcha_results
        :param rel_dict: Dictionary of all required information
        :return: Row count and SQL response
        """
        columns, values = query_tools.insert_string_from_dict(rel_dict)
        sql = f"""
        INSERT INTO coreapp.site_captcha_results
                    ({columns})
        VALUES      ({values})
        """
        response = self.captcha_pg.execute_query(sql)
        assert response[0] == 1
        assert response[1] is None
        return response


class SiteCaptchaResultsReader(object):
    """ Queries for retrieving the records from coreapp.site_captcha_results """

    def __init__(self):
        """ Set up class variables """
        self.captcha_pg = PGUtil(user='app_reader')

    def get_record_for_ip_address(self, ip_address):
        """
        Get the record(s) for a given IP address
        :param ip_address:
        :return:
        """
        sql = f"""
        SELECT   * 
        FROM     coreapp.site_captcha_results 
        WHERE    ipaddress = '{ip_address}' 
        ORDER BY tsCreated DESC
        """
        response = self.captcha_pg.execute_query(sql)
        return response
