# -*- coding: utf-8 -*-
# Author: shenglong
# Date: 2021/1/12

if __name__ == "__main__":
    from flexiv_consul_service.src.client import get_service_info

    res = get_service_info("api/v1/group",
                           "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Ilx1OGMzN1x1NTcyM1x1OWY5OSIsImV4cCI6MTYxMDUyODI4NCwiZW1haWwiOiJzaGVuZ2xvbmcuZ3VAZmxleGl2LmNvbSJ9.vBAHil-VcfcHNZa_kyhH5uoFJ_n8izm1OS6V3S6IN2s")
    print(res)
