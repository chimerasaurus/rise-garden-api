# Imports
import requests
import time

class Gardenapi:
    """
    Class that represets the Rise Garden API.
    
    Attributes
    ----------
    url: Base URL of the Rise Garden API
    token: Login token for the Rise Garden API
    credetials: The email and password used to login
    user_info: User information returned from the Rise Garden API
    
    Methods
    -------
    login(email, password): Log into the Rise Garden API
    get_gardens(): Get a list of the Rise Gardens for the account
    """

    # Initialize the class
    def __init__(self):
        self.url = 'https://prod-api.risegds.com/v2'
        self.token = {
            'access_token': None,
            'refresh_token': None,
            'user_id': None,
            'expires_in': 0,
            'expires_at': 0,
        }
        self.credentials = {
            'email': None,
            'password': None,
        }
        self.user_info = None


    # Private Methods
    def _is_token_expired(self) -> bool:
        return self.token['expires_at'] - 60000 > int(time.time())

    def _is_token_valid(self) -> bool:
        return self.token['access_token'] is not None and not self._is_token_expired()

    def _request(self, method: str, endpoint: str, body: dict = None) -> dict:
        # Check if token is valid if this is not a login
        if (endpoint != '/auth/login' and endpoint != '/auth/refresh_token'):
            self._refresh_token()
        headers = {"Authorization": "Bearer " + self.token['access_token']}
        response = requests.request(
            method,
            headers=headers,
            url=self.url + endpoint,
            data=body,
            timeout=10
        )
        return(response.json())
    
    def _refresh(self) -> None:
        self._request('POST', '/auth/refresh_token')
        return None
    
    def _refresh_token(self) -> None:
        if (self.token['refresh_token'] is not None and self._is_token_expired()):
            self._refresh()
        elif (self.token['refresh_token'] is None):
            self.login(self.credentials['email'], self.credentials['password'])

    # Public Methods
    def login(self, email: str, password: str) -> bool:
        """
        Log into the Rise Garden API with the supplied email and password.
        
        :param email: Login email
        :param password: Login password
        :return: bool. True if login successful; false if unsuccessful.
        """
        self.credentials['email'] = email
        self.credentials['password'] = password

        response = requests.post(f'{self.url}/auth/login', json=self.credentials, timeout=5)
        if response.status_code != 200:
            print(response)
            return False

        print(response.json())
        self.token['access_token'] = response.json()['token']
        self.token['refresh_token'] = response.json()['refresh_token']
        self.token['user_id'] = response.json()['user']['id']
        self.token['expires_in'] = response.json()['expires_in']
        self.token['expires_at'] = response.json()['expires_in'] + int(time.time())

        return True

    def get_gardens(self) -> dict:
        """
        Get a list of gardens managed / owned by the account
        
        :return: list of gardens managed by the account
        """
        return self._request('GET', '/gardens')

