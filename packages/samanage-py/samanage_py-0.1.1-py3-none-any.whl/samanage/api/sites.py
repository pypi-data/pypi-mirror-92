from samanage import Samanage

class Site(Samanage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_url = self.options.get('site') 

    def create_site(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dict.")

        path = f'{self.base_url}/{self.resource_url}'
        return self.create(path, payload)

    def get_site(self, id, layout=None):
        path = f'{self.base_url}/sites/{id}.json'
        if layout:
            path = path + '?layout=long'
        return self.get(path)

    def get_all_sites(self, layout=None):
        path = f"{self.base_url}/{self.resource_url}"
        if layout:
            path = path + '?layout=long'
        return super().get_all(path)

    def update_site(self, payload):
        path = f"/{self.resource_url}"
        return self.update(path, payload)

    def delete_site(self, id):
        path = f'/sites/{id}.json'
        return self.delete(path)