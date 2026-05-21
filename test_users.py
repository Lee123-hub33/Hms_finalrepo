#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import sys

BASE = 'http://localhost:8000'

# Login
try:
    data = urllib.parse.urlencode({'grant_type': 'password', 'username': 'testuser', 'password': 'TestPass123'}).encode('utf-8')
    req = urllib.request.Request(f'{BASE}/auth/token', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req) as r:
        resp = json.load(r)
    token = resp['access_token']
    print(f'Got token for testuser')
except Exception as e:
    print(f'Login failed: {e}')
    sys.exit(1)

# GET /users
try:
    req = urllib.request.Request(f'{BASE}/users', headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req) as r:
        users = json.load(r)
    print(f'SUCCESS: Retrieved {len(users)} users')
    for u in users:
        print(f'  - {u["username"]} (id={u["id"]}, active={u["is_active"]})')
except urllib.error.HTTPError as e:
    print(f'FAILED: {e.code}')
    body = e.read().decode()
    print(json.loads(body))
