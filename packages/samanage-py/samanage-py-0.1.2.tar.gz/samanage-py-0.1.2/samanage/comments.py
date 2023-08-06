import logging

from samanage import Samanage

logger = logging.getLogger(__name__)

class Comment(Samanage):
    _endpoints = {
        'comment': '/comments/{id}.json',
        'comments': '/comments.json',
    }

    def __init__(self, parent=None, record=None, *args, **kwargs):
        self.base_url = parent.base_url
        self.con = parent.con

    def create(self, parent_id, **kwargs):
        path = f"{self.base_url}/incidents/{parent_id}{self._endpoints.get('comments')}"
        return self.con.post(path, **kwargs)

    def get(self, id):
        path = self.base_url + self._endpoints.get('comment').format(id=id)
        return self.con.get(path)

    def update(self, id, payload):
        path = self.base_url + self._endpoints.get('comment').format(id=id)
        return self.con.update(path, payload)

    def delete(self):
        path = self.base_url + self._endpoints.get('comment').format(id=id)
        return self.con.delete(path)
