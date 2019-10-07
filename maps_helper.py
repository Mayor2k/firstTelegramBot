import json
import requests


response = requests.get("https://places.cit.api.here.com/places/v1/autosuggest?at=56.114526%2C47.198588&q=почта&Accept-Language=en-US%3Ben&app_id=x2p3TDHxbG04n0y1cC9j&app_code=gRs6qSR72e0_-k_nLMgP7A")
todos = json.loads(response.text)
xd_list = []
for x in range(len(todos.get('results'))):
    if todos.get('results')[x].get('category') == 'post-office':
        xd_list.append(todos.get('results')[x].get('distance'))
    else:
        xd_list.append(0)
closest_mail = min(x for x in xd_list if x != 0)
print(todos.get('results')[xd_list.index(closest_mail)].get('title'))
print(todos.get('results')[xd_list.index(closest_mail)].get('position'))
