import json
a= [{"id":1,"name":"获取用户列表1","path":"/users/admin/search?targetOrgId=","method":"POST","status":1,"index":1},{"id":2,"name":"获取用户列表2","path":"/users/admin/search?targetOrgId=","method":"POST","status":1,"index":2}]

print(json.dumps(a))
