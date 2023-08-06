"""Stream4good/Discoverability API Wrapper."""
import requests


class S4GAPI:
    """This class wraps stream4good/discoverability Rest API."""

    ROOT_DNS = 'vod-prime.space'
    PROTOCOL = 'https'
    REALM = 'discoverability'
    ACCESS_TOKEN_URL = f'/auth/realms/{REALM}/protocol/openid-connect/token'

    def __init__(self, user,
                 password,
                 client_id='dashboard-vuejs',
                 scope='dashboard-vuejs'):
        """Create an initilize the API."""
        self.user = user
        self.password = password
        self.session = requests.Session()
        payload = {'client_id': client_id,
                   'grant_type': 'password',
                   'scope': scope,
                   'username': self.user,
                   'password': self.password}
        resp = self.session.post(
            f'{S4GAPI.PROTOCOL}://auth.{ S4GAPI.ROOT_DNS}'
            + f'/auth/realms/{S4GAPI.REALM}'
            + '/protocol/openid-connect/token',
            data=payload)
        self.access_token = resp.json()['access_token']
        self.authorization_header =  \
            {'Authorization':
                f'Bearer {self.access_token}'}

    def get_credentials(self, provider):
        """Get a tuple containing credentials for the supplied provider."""
        credentials = self.session.get(
            f'{S4GAPI.PROTOCOL}://'
            + f'credentials.{S4GAPI.ROOT_DNS}'
            + f'/providers/{provider}',
            headers=self.authorization_header).json()
        single_credentials_link = credentials['links'][0]['href']

        single_credentials = self.session.get(
            single_credentials_link,
            headers=self.authorization_header).json()
        login = single_credentials['credentials']['login']
        password = single_credentials['credentials']['password']
        return login, password
