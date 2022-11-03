import logging
from aiohttp_jinja2 import template

from app.service.auth_svc import for_all_public_methods, check_authorization
from app.utility.base_world import BaseWorld
from plugins.manncmd.app.manncmd_svc import ManncmdService


@for_all_public_methods(check_authorization)
class ManncmdGUI(BaseWorld):

    def __init__(self, services, name, description):
        self.name = name
        self.description = description
        self.services = services
        self.manncmd_svc = ManncmdService(services)

        self.auth_svc = services.get('auth_svc')
        self.log = logging.getLogger('manncmd_gui')

    @template('manncmd.html')
    async def splash(self, request):
        return dict(name=self.name, description=self.description)

    # Add functions here that the front-end will use

