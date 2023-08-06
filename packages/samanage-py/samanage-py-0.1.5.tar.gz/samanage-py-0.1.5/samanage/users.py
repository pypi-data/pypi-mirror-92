import logging
from samanage import incidents

from samanage import Samanage
from samanage.incidents import IncidentRecord

logger = logging.getLogger(__name__)

class UserRecord(IncidentRecord):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    def __repr__(self):
        super().__repr__()
        return f"<User: {self.id}>"

class User:
    _endpoints = {
        'users': '/users.json',
        'user': '/users/{id}.json'
    }

    _required_fields = (
        'email',
    )

    user_constructor = UserRecord

    def __init__(self, parent=None, *args, **kwargs):
        if parent is None:
            raise ValueError('Parent is not specified.')
        self.con = parent.con
        self.base_url = parent.base_url

    def get(self, id, params=None):
        path = self.base_url + self._endpoints.get('user').format(id=id)
        response = self.con.get(path, params=params)

        if not response:
            return None
        data = response.json()
        return self.user_constructor(**data)
