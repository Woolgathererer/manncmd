from app.utility.base_world import BaseWorld
from plugins.manncmd.app.manncmd_gui import ManncmdGUI
from plugins.manncmd.app.manncmd_api import ManncmdAPI


name = 'Manncmd'
description = 'manncmdv1.0'
address = '/plugin/manncmd/gui'
access = BaseWorld.Access.RED


async def enable(services):
    app = services.get('app_svc').application
    manncmd_gui = ManncmdGUI(services, name=name, description=description)
    app.router.add_static('/manncmd', 'plugins/manncmd/static/', append_version=True)
    app.router.add_route('GET', '/plugin/manncmd/gui', manncmd_gui.splash)

    manncmd_api = ManncmdAPI(services)
    # Add API routes here
    app.router.add_route('POST', '/plugin/manncmd/mirror', manncmd_api.mirror)

    app.router.add_route('POST', '/plugin/manncmd/get_info', manncmd_api.get_info)
    app.router.add_route('POST', '/plugin/manncmd/exploit', manncmd_api.exploit)
    app.router.add_route('POST', '/plugin/manncmd/deploy_cve', manncmd_api.deploy_cve)
    app.router.add_route('POST', '/plugin/manncmd/detect_res', manncmd_api.detect_res)

