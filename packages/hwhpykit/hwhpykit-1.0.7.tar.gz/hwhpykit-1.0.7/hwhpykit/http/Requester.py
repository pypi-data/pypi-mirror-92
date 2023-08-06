

import requests
import demjson
import json


class Requester(object):
    """ 请求者 """
    @classmethod
    def get_request(cls, url, headers={}, print_content=False):
        try:
            resp = requests.get(url, headers)
            return demjson.decode(resp.text)
        except Exception as e:
            print(e)
            return ""

    @classmethod
    def post_request(cls, url, parameters={}, headers={}, print_content=False):
        data = json.dumps(parameters)
        try:
            resp = requests.post(url, data=data, headers=headers)

            try:
                resp_json = demjson.decode(resp.text)
                return json.dumps(resp_json, indent=4, sort_keys=True)
            except Exception as e:
                print(e)
                return ""
        except Exception as e:
            print(e)
            return ""

