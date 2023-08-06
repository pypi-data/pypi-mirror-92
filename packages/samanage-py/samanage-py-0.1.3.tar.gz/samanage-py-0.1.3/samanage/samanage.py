import logging
from .connection import Connection

logger = logging.getLogger(__name__)

SAMANAGE_API_VERSION = 'v2.1'
SAMANAGE_BASE_URL = 'https://api.samanage.com'

class Samanage:

    connection_constructor = Connection

    def __init__(self, token, base_url=None, **kwargs):

        headers = kwargs.get('headers', None)
        if token:
            if headers is None:
                kwargs['headers'] = {
                    'Accept': f'application/vnd.samanage.{SAMANAGE_API_VERSION}+json',
                    'Content-Type': 'application/json',
                    'X-Samanage-Authorization': f'Bearer {token}',
                }
            self.con = self.connection_constructor(token, **kwargs)
        else:
            raise ValueError("Token must be provided.") 

        if base_url is None:
            self.base_url = SAMANAGE_BASE_URL 
        else:
            self.base_url = base_url

    def incident(self, **kwargs):
        from .incidents import Incident
        return Incident(parent=self)

    def comment(self, **kwargs):
        from .comments import Comment 
        return Comment(parent=self)

    def change(self, **kwargs):
        pass

    def user(self, **kwargs):
        from .users import User
        return User(parent=self)

    def site(self, **kwargs):
        from .sites import Site
        return Site(parent=self) 