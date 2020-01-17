# -*- coding: utf-8 -*-

import requests
import json


def execute(request_data, path="/", port=5001, host="127.0.0.1"):
    url = "http://{host}:{port}{path}".format(host=host, port=port, path=path)
    request_data["sign"] = "waterworldwaterworldwaterworld"
    response = requests.post(url, data=request_data)
    if response.status_code != 200:
        response.raise_for_status()
    cost_time = round(response.elapsed.total_seconds() * 1000, 2)
    response = response.json()
    print("\n=====================response==================================")
    print("\033[0;36m{}\033[0m".format(
        json.dumps(response, ensure_ascii=False, indent=4)))
    print("\n响应时间: {} ms".format(cost_time))
    print("=====================response==================================\n")
