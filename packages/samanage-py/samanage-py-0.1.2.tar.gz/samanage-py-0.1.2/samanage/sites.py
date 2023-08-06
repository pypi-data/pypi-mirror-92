import logging

logger = logging.getLogger(__name__)

class Site:
    _endpoints = {
        'site': '/sites/{id}.json',
        'sites': '/sites.json',
    }

    _required_fields = (
        'site'
    )

    def __init__(self, parent=None, *args, **kwargs):
        self.con = parent.con
        self.base_url = parent.base_url

    def get(self, id, params=None):
        """Return a single site."""
        path = self.base_url + self._endpoints.get('site').format(id=id)
        response = self.con.get(path, params=params if params else None)
        if not response:
            return None
        return response.json()

    def get_all(self, params=None):
        """
        Return all sites.
        """
        collections = None
        path = self.base_url + self._endpoints.get('sites')

        response = self.con.get(path, params=params if params else None)
        collections=response.json()
        while 'next' in response.links:
            response = self.con.get(response.links['next']['url'], params=params if params else None) 
            collections.extend(response.json())

        return collections

    def create(self, data):
        path = self.base_url + self._endpoints.get('sites')
        if isinstance(data, dict):
            if 'site' in data:
                if self._required_fields not in data.get('site'):
                    raise ValueError('Fields: ' + ', '.join(self._required_fields) + ' is required.')
        else:
            raise TypeError('Payload must be a dict.')
        return self.con.create(path, data=data)

    def update(self, id, payload):
        path = self.base_url + self._endpoints.get('site').format(id=id)

        if not isinstance(payload, dict):
            raise ValueError('Payload must be a dict.')
        return self.con.put(path, json=payload)

    def delete(self, id):
        path = self.base_url + self._endpoints.get('site').format(id=id)
        return self.con.delete(path)


        
