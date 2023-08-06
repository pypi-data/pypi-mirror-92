import logging

from enum import Enum

logger = logging.getLogger(__name__)

class Resource(Enum):
    CATALOG = 'incidents' 
    CHANGE = 'changes' 
    COMMENT = 'incidents' 
    INCIDENT = 'incidents' 
    PROBLEM = 'problems' 
    SITE= 'sites' 
    USER = 'users' 

class BaseApi:
    """ Base class for all interaction with Samanage API """

    def __init__(self, resource=None, **kwargs):
        # self._base_url = build_base_url() 

    def build_url(self, endpoint):
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        return f"{self._base_url}/{endpoint}"

    def build_url(self):
        pass