"""Stream4good/Discoverability API Wrapper."""
from urllib.parse import urljoin
import requests
from requests import Session



class ConsoAPI:
    """This class wraps the conso-api."""

    def __init__(self, session):
        """Initialize a new ConsoAPI.

        It works by inheriting from the session object of a S4GAPI.
        """
        self.session = session

    def create_direct_schedule(self, airing_time, video_id):
        """Publish or updated a new direct schedule."""
        self.session.post('/direct',
            json=[{'airing_time': airing_time, 'video_id': video_id}])


class UserAPI:
    """This class wraps the user API"""

    def __init__(self, session):
        """intialiaze a new Credential API"""
        self.session = session

    def get_users(self):
        """returns a list of users."""
        resp= self.session.get("/api/users")
        return resp.json()

    def get_user(self,user_id):
        return self.session.get(f"/api/user/{user_id}").json()



class CredentialAPI():
    """Wraps credential API."""

    def __init__(self, session):
        """intialiaze a new Credential API"""
        self.session = session

    def get_credentials(self, provider):
        """Get a tuple containing credentials for the supplied provider."""
        credentials = self.session.get(f'/providers/{provider}').json()
        single_credentials_link = credentials['links'][0]['href']

        single_credentials = self.session.get(
            single_credentials_link,
        ).json()
        login = single_credentials['credentials']['login']
        password = single_credentials['credentials']['password']
        return login, password


class S4GSession(Session):
    """Wraps a session to provide API baseline."""
    def __init__(self, prefix_url, access_token=None):
        """initialize baseline for API"""
        self.prefix_url = prefix_url
        self.access_token = access_token
        super(S4GSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        if self.access_token is not None:
            if 'headers' in kwargs:
                headers = kwargs["headers"]
            else:
                headers = {}
                kwargs["headers"] = headers
            headers.update(
                {'Authorization':
                 f'Bearer {self.access_token}'})
        return super(S4GSession, self).request(method,
                                               url,
                                               *args,
                                               **kwargs)


class S4GAPI:
    """This class wraps stream4good/discoverability Rest API."""

    def __init__(self, user,
                 password,
                 client_id='dashboard-vuejs',
                 scope='dashboard-vuejs',
                 root_dns='vod-prime.space',
                 protocol='https',
                 realm='discoverability'):
        """Create an initilize the API."""
        self.user = user
        self.password = password
        self.root_dns = root_dns
        self.protocol = protocol
        self.realm = realm
        self.access_token_url =\
            f'/auth/realms/{self.realm}/protocol/openid-connect/token'
        payload = {'client_id': client_id,
                   'grant_type': 'password',
                   'scope': scope,
                   'username': self.user,
                   'password': self.password}
        self.session = requests.Session()
        resp = self.session.post(
            f'{self.protocol}://auth.{self.root_dns}'
            + f'/auth/realms/{self.realm}'
            + '/protocol/openid-connect/token',
            data=payload)
        self.access_token = resp.json()['access_token']

    def get_credentials_api(self):
        """Returns a configured instance of CredentialAPI"""
        return CredentialAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://credentials.{self.root_dns}',
                access_token=self.access_token))

    def get_conso_api(self):
        """Return a configured instance of the ConsoAPI."""
        return ConsoAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://conso-api.{self.root_dns}',
                access_token=self.access_token))

    def get_user_api(self):
        """Return a configured instance of the ConsoAPI."""
        return UserAPI(
            S4GSession(
                prefix_url=f'{self.protocol}://api.{self.root_dns}',
                access_token=self.access_token))
