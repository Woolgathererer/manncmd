import json
import threading
import uuid


from aiohttp import web


from app.objects.c_ability import AbilitySchema
from app.objects.secondclass.c_executor import Executor, ExecutorSchema
from app.service.auth_svc import for_all_public_methods, check_authorization
from app.objects.secondclass.c_fact import Fact
from app.objects.c_agent import Agent
from plugins.manncmd.app import manncmd_CVEs
from plugins.manncmd.app import manncmd_server


@for_all_public_methods(check_authorization)
class ManncmdAPI:

    def __init__(self, services):
        self.services = services
        self.auth_svc = self.services.get('auth_svc')
        self.data_svc = self.services.get('data_svc')
        self.rest_svc = self.services.get('rest_svc')
        thread = threading.Thread(target=manncmd_server.run)
        thread.start()

    async def mirror(self, request):
        """
        This sample endpoint mirrors the request body in its response
        """
        request_body = json.loads(await request.read())
        return web.json_response(request_body)

    async def exploit(self, request):
        data = await request.json()
        converted_facts = [Fact(trait=f['trait'], value=f['value']) for f in data.get('facts', [])]

        await self.task_agent_with_ability_test(data['paw'], data, data['obfuscator'], converted_facts)
        return web.json_response('complete')

    async def task_agent_with_ability_test(self, paw, data, obfuscator, facts=()):
        new_links = []
        name = data.get('name')
        for agent in await self.rest_svc.get_service('data_svc').locate('agents', dict(paw=paw)):
            executor = await self.creat_executor(data=data.pop('executor', {}), agent=agent)
            ability = await self.create_ability(name=name, data=data.pop('ability', {}), executor=executor)
            abilities = [ability]
            links = await agent.task(
                abilities=abilities,
                obfuscator=obfuscator,
                facts=facts
            )
            new_links.extend(links)
        return new_links

    async def creat_executor(self, data: dict, agent: Agent):
        if not data.get('timeout'):
            data['timeout'] = 60
        data['platform'] = agent.platform
        executor = ExecutorSchema().load(data)
        return executor

    async def create_ability(self, name, data: dict, executor: Executor):
        if not data.get('ability_id'):
            data['ability_id'] = str(uuid.uuid4())
        if not data.get('tactic'):
            data['tactic'] = 'auto-generated'
        if not data.get('technique_id'):
            data['technique_id'] = 'auto-generated'
        if not data.get('technique_name'):
            data['technique_name'] = 'auto-generated'
        if not name:
            data['name'] = 'Manual Command'
        else:
            data['name'] = name
        if not data.get('description'):
            data['description'] = 'Manual command ability'
        data['executors'] = [ExecutorSchema().dump(executor)]
        ability = AbilitySchema().load(data)
        return ability


    async def get_info(self, request):
        data = await request.json()
        if not data.get('CVE_platform'):
            res = await manncmd_CVEs.as_list_platform()
            print(res)
            return web.json_response(res)
        if not data.get('CVEs'):
            res = await manncmd_CVEs.as_list_cve(data.get('CVE_platform'))
            return web.json_response(res)
        if data.get('SetFlag'):
            res = await manncmd_CVEs.Set_flags(data.get('CVE_platform'), data.get('CVEs'))
            return web.json_response(res)
        return web.json_response('complete')

    async def deploy_cve(self, request):
        data = await request.json()

        if not data.get('flag'):
            return web.json_response('wrong operation')
        flag = data.get('flag')
        res = await manncmd_CVEs.as_construct_command(data)
        # print(data['executor']['command'])
        data['executor']['command'] = res
        # print(data['executor']['command'])
        if flag == 'description':
            return web.json_response(res)
        else:
            converted_facts = [Fact(trait=f['trait'], value=f['value']) for f in data.get('facts', [])]
            await self.task_agent_with_ability_test(data['paw'], data, data['obfuscator'], converted_facts)
            return web.json_response(res)

    async def detect_res(self,request):
        data = await request.json()
        await manncmd_CVEs.as_export_report(data)

        return web.json_response('complete')


