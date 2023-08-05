# -*- coding: utf-8 -*-
# Author: shenglong
# Date: 2021/1/12

import consul
import requests
import json
from random import randint

from flexiv_consul_service.conf import settings as service_center_settings


class ConsulBaseService:
    _instance = None

    def __init__(self):
        self.host = service_center_settings.CONSUL_IP
        self.port = service_center_settings.CONSUL_PORT
        self.token = service_center_settings.CONSUL_TOKEN
        self.consul = consul.Consul(host=self.host, port=self.port)

    def __call__(cls):
        if not cls._instance:
            cls._instance = ConsulBaseService()
        return cls._instance

    def register(self, name, service_id, address, port, tags):  # 注册服务 注册服务的服务名  端口  以及 健康监测端口
        self.consul.agent.service.register(name, service_id=service_id, address=address, port=port, tags=tags,
                                           check=consul.Check().tcp(self.host, self.port, "10s", "10s", '10s'))

    def get_service(self, name):
        # 获取相应服务下的 DataCenter
        url = 'http://' + self.host + ':' + str(self.port) + '/v1/catalog/service/' + name
        service_center_resp = requests.get(url)
        if service_center_resp.status_code != 200:
            raise Exception('can not connect to consul ')
        service_info_list = json.loads(service_center_resp.text)
        # 初始化 DataCenter
        temp_set = set()
        for service in service_info_list:
            temp_set.add(service.get('Datacenter'))
        # 服务列表初始化
        service_list = []
        for dc in temp_set:
            if self.token:
                url = f'http://{self.host}:{self.port}/v1/health/service/{name}?dc={dc}&token={self.token}'
            else:
                url = f'http://{self.host}:{self.port}/v1/health/service/{name}?dc={dc}&token='
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception('can not connect to consul ')
            text = resp.text
            service_list_data = json.loads(text)

            for serv in service_list_data:
                status = serv.get('Checks')[1].get('Status')
                # 选取成功的节点
                if status == 'passing':
                    address = serv.get('Service').get('Address')
                    port = serv.get('Service').get('Port')
                    service_list.append({'port': port, 'address': address})
        if len(service_list) == 0:
            raise Exception('no service can be used')
        else:
            service = service_list[randint(0, len(service_list) - 1)]
            return service['address'], int(service['port'])
