import requests

class ConnectApi:
    def __init__(self, host, secret_key):
        self.host = host
        self.secret_key = secret_key
    
    def create_code(self, username):
        r = requests.post(self.host + "code/", data={
            'secret_key': self.secret_key,
            'username': username
        })
        return r.json()
    
    def register(self, code, password):
        r = requests.post(self.host + "register/", data={
            'code': code,
            'password': password
        })
        return r.json()

class KoperApi:
    def __init__(self):
        self.hosts = {
            'connect': 'https://koperpapilavomerka.herokuapp.com/api/v1/connect/',
            'bank': 'https://koperpapilavomerka.herokuapp.com/api/v1/bank/'
        }
        self.connect = ConnectApi(self.hosts['connect'], "django-insecure-n$r^s@#zln#9tyenczf4r%qd5o#-#&)(!q#^)m$x6hi!8snsic")
