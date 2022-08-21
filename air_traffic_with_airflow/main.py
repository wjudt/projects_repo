import requests
from requests.auth import HTTPBasicAuth

response = requests.get("https://opensky-network.org/api",
                        auth=HTTPBasicAuth('wjudt', 'tupolew1004!'))
print(response)





if __name__ == '__main__':
    pass

