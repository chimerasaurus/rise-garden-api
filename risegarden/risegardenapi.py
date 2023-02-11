# Imports
import json
import time
import requests
from risegarden.garden import Garden

class RiseGardenAPI:
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
        self.timeout = 20
        self.gardens = []


    # Private Methods
    def _is_token_expired(self) -> bool:
        """
        PRIVATE: Check whether the token is expired; toklen doesn't expire in next 60 seconds.

        :return: bool. True if token is expired; false if token is valid.
        """
        return self.token['expires_at'] - 60000 < int(time.time())

    def _is_token_valid(self) -> bool:
        """
        PRIVATE: Check whether the token is valid. Ensures the token is not expired and is not None.

        :return: bool. True if token is valid; false if token is invalid.
        """
        return self.token['access_token'] is not None and not self._is_token_expired()

    def _request(self, method: str, endpoint: str, body: dict = None) -> dict:
        """
        PRIVATE: Make a request to the Rise Garden API.

        :param method: HTTP method to use (eg: GET, POST, etc.)
        :param endpoint: Endpoint to make the request to
        :param body: Body of the request
        :return: dict of the response from the API
        """
        # Check if token is valid if this is not a login
        if (endpoint != '/auth/login' and endpoint != '/auth/refresh_token'):
            self._refresh_token()
        headers = {"Authorization": "Bearer " + self.token['access_token']}
        response = requests.request(
            method,
            headers=headers,
            url=self.url + endpoint,
            data=json.dumps(body),
            timeout=self.timeout
        )
        return (response.json(), response.status_code)

    def _refresh(self) -> bool:
        """
        PRIVATE: Refresh the token.
        :return: bool. True if token refreshed; false if token not refreshed.
        """
        # TODO Missing token
        response = self._request('POST', '/auth/refresh_token')
        if response[1] != 200:
            return False
        return True

    def _refresh_token(self) -> None:
        """
        PRIVATE: Refresh the token if it is expired or invalid.
        """
        if (self.token['refresh_token'] is not None and self._is_token_expired()):
            self._refresh()
        elif self.token['refresh_token'] is None:
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

        response = requests.post(f'{self.url}/auth/login', json=self.credentials, timeout=self.timeout)
        if response.status_code != 200:
            return False

        self.token['access_token'] = response.json()['token']
        self.token['refresh_token'] = response.json()['refresh_token']
        self.token['expires_in'] = response.json()['expires_in']
        self.token['expires_at'] = response.json()['expires_in'] + int(time.time())
        self.user_info = response.json()['user']

        return True

    def get_garden_status(self, garden_id: int) -> dict:
        """
        Get the status of a garden (eg: lights, temperature, etc.)

        :param garden_id: Garden to get information for (ID is from get_tardens)
        :return: dict of garden details
        """
        garden_details = self._request('GET', f'/gardens/{garden_id}/device/status')
        return garden_details[0]

    def get_gardens(self) -> list:
        """
        Get a list of gardens managed / owned by the account

        :return: list of gardens managed by the account
        """
        response = self._request('GET', '/gardens')
        # Add the garden to the list
        for rise_garden in response[0]:
            new_garden = Garden(rise_garden['id'], rise_garden['name'], rise_garden['garden_type'], self)
            self.gardens.append(new_garden)
        return response[0]

    def set_lamp_level(self, number: int, level: int) -> bool:
        """
        Set the lamp level for the garden.
        :param id: number of the garden
        :param level: Level to set the lamp to (0-100)
        :return: bool. True if successful; false if unsuccessful.
        """
        request_body = {
            "light_level": str(level),
            "wait_for_response": "true"
        }
        response = self._request('PUT', f'/gardens/{number}/device/light-level', request_body)
        if response[1] != 200:
            return False
        # Update the status of the garden now that the state has changed
        self.update_garden(number)
        return True

    def update_garden(self, number: int) -> bool:
        """
        Update the status for a specific garden.
        :param id: ID of the garden to update
        :return: bool. True if successful; false if unsuccessful.
        """
        for rise_garden in self.gardens:
            if rise_garden.number == number:
                rise_garden.update()
        return True

    def update_gardens(self) -> bool:
        """
        Update the status for each garden in the list of gardens.
        :return: bool. True if successful; false if unsuccessful.
        """
        # Get gardens if there are none
        if len(self.gardens) == 0:
            self.get_gardens()

        # Update each garden
        for rise_garden in self.gardens:
            rise_garden.update()
        return True
