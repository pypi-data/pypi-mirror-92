import logging

from samanage import Samanage

logger = logging.getLogger(__name__)

class IncidentRecord:
    """
        TODO:  
    """
    def __init__(self, parent=None, **kwargs):
        self.number = kwargs.get('number', None)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Incident: {self.number}>" 

    
class Incident:
    _endpoints = {
        'incidents': '/incidents.json',
        'get_incident': '/incidents/{id}.json',
        'search': '/search.json?q={keyword}',
    }

    _required_fields = (
        'name',
        'requester',
        'priority',
    )

    incident_constructor = IncidentRecord

    def __init__(self, parent=None, *args, **kwargs):

        if parent is None:
            raise ValueError('Parent not specified.')
        self.con = parent.con
        self.base_url = parent.base_url

    def get(self, id, params=None, layout=None):
        """
            Return a single incident or page
        """
        path = 'https://api.samanage.com' + self._endpoints.get('get_incident').format(id=id)
        if layout:
            path = path + '?layout=long'
        response = self.con.get(path, params=params if params else None)

        if not response:
            return None
        data = response.json()
        return self.incident_constructor(**data) 

    def get_all(self, url=None, params=None, layout=None):
        """
            Return all incidents based on the url provided.
        """
        collections=None

        if url is None:
            path = 'https://api.samanage.com' + self._endpoints.get('incidents')
        else:
            path = url

        response = self.con.get(path, params=params if params else None)
        collections=response.json()
        while 'next' in response.links:
            response = self.con.get(response.links['next']['url'], params=params if params else None) 
            collections.extend(response.json())
        if not response:
            return None
        return [self.incident_constructor(**incident) for incident in collections]

    def search(self, keyword, **params):
        path = self.base_url + self._endpoints.get('search').format(keyword=keyword)
        self.con.get(path)

    def create(self, data):
        path = self.base_url + self._endpoints.get('incidents')

        if isinstance(data, dict):
            if 'incident' in data:
                if self._required_fields not in data.get('incident'):
                    raise ValueError('Fields: ' + ', '.join(self._required_fields) + ' is required.')
        else:
            raise TypeError('Payload must be a dict.')
        return self.con.create(path, data=data)

    def update(self, id, payload):
        path = self.base_url + self._endpoints.get('get_incident').format(id=id)

        if not isinstance(payload, dict):
            raise ValueError('Payload must be a dict.')
        return self.con.put(path, json=payload)

    def delete(self, id):
        path = self.base_url + self._endpoints.get('get_incident').format(id=id)
        return self.con.delete(path)

    def filter(self):
        pass
