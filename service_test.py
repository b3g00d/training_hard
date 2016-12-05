import requests


URL = 'http://127.0.0.1:5000'
param = {'filename':
         'anarchy.jpg'}
print requests.post(URL, params=param)
