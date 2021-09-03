from models import tls_feature
import json
a = [[0,0,0,0],[1,1,1,1],[2,2,2,2]]
a = json.dumps(a)
t = tls_feature(client_hello=a, server_hello=a, certificiate=a, name='1')
t.save()