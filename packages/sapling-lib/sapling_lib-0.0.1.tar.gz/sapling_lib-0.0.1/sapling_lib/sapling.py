""" Sapling Module
"""
from datetime import datetime, timedelta
import requests


class Sapling:
    def __init__(self, uri, api_key):
        self.get_header = {'Authorization': f'Token {api_key}'}
        self.put_header = {'Authorization': f'Token {api_key}',
                           "Content-Type": "application/x-www-form-urlencoded"
                           }
        self.uri = uri

    def get_users(self, max_days=1):
        """Gets user from sapling

        Keyword Arguments:
            max_days {int} -- Maximum days from current date to retrieve user (default: {1})

        Returns:
            [type] -- [description]
        """
        now = datetime.now().date().strftime('%Y-%m-%d')
        print(now)
        till = (datetime.now() + timedelta(days=max_days)
                ).date().strftime('%Y-%m-%d')
        url = f'https://{self.uri}.saplingapp.io/api/v1/beta/profiles?status=active' + \
            f'&start_date[since]={now}&start_date[until]={till}'
        response = requests.get(url, headers=self.get_header)
        return response.json()['users']

    def get_users_backdate(self, max_days=1):
        """Gets user from sapling

        Keyword Arguments:
            max_days {int} -- Maximum days from current date to retrieve user (default: {1})

        Returns:
            [type] -- [description]
        """
        page = 1
        end = datetime.now().date().strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=max_days)
                 ).date().strftime('%Y-%m-%d')
        print(start, end)
        url = f'https://{self.uri}.saplingapp.io/api/v1/beta/profiles?status=active' + \
            f'&start_date[since]={start}&start_date[until]={end}&page={page}'
        response = requests.get(url, headers=self.get_header)
        users = response.json()['users']
        page += 1

        while(True):
            if page <= response.json()['total_pages']:
                url = f'https://{self.uri}.saplingapp.io/api/v1/beta/profiles?status=active' +\
                      f'&start_date[since]={start}&start_date[until]={end}&page={page}'
                response = requests.get(url, headers=self.get_header)
                users += response.json()['users']
                print(response.json()['current_page'])
                page += 1
                continue
            break
        return users

    def get_user_by_guid(self, guid):
        """Get user by guid

        Arguments:
            guid {str} -- Unique identifier for user

        Returns:
            dict -- User data
        """
        url = f'https://{self.uri}.saplingapp.io/api/v1/beta/profiles/{guid}'
        response = requests.get(url, headers=self.get_header)
        return response.json()

    def update_email(self, guid, email):
        """Update Company Email for user

        Arguments:
            guid {str} -- Unique identifier
            email {str} -- User email

        Returns:
            int -- status code
        """
        url = f'https://{self.uri}.saplingapp.io/api/v1/beta/profiles/{guid}'
        response = requests.put(url, headers=self.put_header, data={
                                'company_email': email})
        return response.status_code
