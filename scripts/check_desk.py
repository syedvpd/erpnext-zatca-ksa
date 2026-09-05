import requests, re

s = requests.Session()
login_res = s.post('http://frontend:8080/api/method/login', data={'usr': 'Administrator', 'pwd': 'admin'})
print('Login response:', login_res.json())

desk_res = s.get('http://frontend:8080/app/home')
print('Desk status:', desk_res.status_code)

tags = re.findall(r'(?:src|href)=["\'](/[^"\']+)["\']', desk_res.text)
print('Assets referenced on /app/home:')
for t in set(tags):
    if any(t.endswith(ext) or ext in t for ext in ['.css', '.js', '.svg', '.png']):
        r = s.get('http://frontend:8080' + t)
        print(f'  {t} -> HTTP {r.status_code} ({len(r.content)} bytes)')
