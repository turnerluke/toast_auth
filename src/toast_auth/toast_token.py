import os
from collections.abc import Mapping
import datetime as dt

import requests
from botocore.exceptions import ClientError


from storage import get_token

token_filename = 'toast_token.json'


class ToastToken(Mapping):
    """
    The ToastToken class stores the Toast API token and expiration date.
    It is a subclass of Mapping, so it can be unpacked like a dictionary.
    The token is stored in a JSON file, and is refreshed when
    the expiration date is reached.

    Using the unpacking operator:
        token = ToastToken()
        payload = {
            'locationGuid': '1234567890',
            'startDate': '2020-01-01',
            'endDate': '2020-01-02',
            **token  # Returns {"Authorization": token}
        }

    """

    def __init__(self, token_location='local'):
        if token_location == 'local':
            self.open_token_json = get_token.token_from_local_file
            self.write_token = get_token.token_to_local_file
        elif token_location == 's3':
            self.open_token_json = get_token.token_from_s3_bucket
            self.write_token = get_token.token_to_s3_bucket

        self._token, self._expiration = self.get_toast_token()
        # self._token is of the form: str - "Bearer: <token>"
        # self._expiration is a datetime object

    def to_dict(self):
        return {'Authorization': self.token}

    def __getitem__(self, key):
        return self.to_dict()[key]

    def __iter__(self):
        return iter(self.to_dict())

    def __len__(self):
        return len(self.to_dict())  # Always 1

    def write_token_json(self, token: str, expires: dt.datetime) -> None:
        data = {
            'Authorization': f"Bearer {token}",
            'Expires': expires.isoformat(),
        }
        self.write_token(data)

    def get_toast_token(self):
        try:
            token = self.open_token_json()
            expires = dt.datetime.fromisoformat(token['Expires'])
            if expires > (dt.datetime.now() + dt.timedelta(minutes=1)):
                return token['Authorization'], expires
            raise FileNotFoundError
        except (FileNotFoundError, ClientError):
            url = f'{os.environ.get("TOAST_API_SERVER")}/authentication/v1/authentication/login'

            payload = {
                "clientId": os.environ.get('TOAST_CLIENT_ID'),
                "clientSecret": os.environ.get('TOAST_CLIENT_SECRET'),
                "userAccessType": "TOAST_MACHINE_CLIENT"
            }

            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)

            data = response.json()
            if data['status'] == 401:
                raise ValueError("Invalid Toast credentials.")
            token = data['token']['accessToken']

            expires = dt.datetime.now() + dt.timedelta(seconds=data['token']['expiresIn'])
            self.write_token_json(token, expires)
            return f"Bearer {token}", expires

    @property
    def token(self):
        if self._expiration < (dt.datetime.now() - dt.timedelta(minutes=1)):
            self._token, self._expiration = self.get_toast_token()
        return self._token

    @token.setter
    def token(self, value):
        raise AttributeError("Cannot overwrite the Toast Token.")
