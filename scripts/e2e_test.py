#!/usr/bin/env python3
import urllib.request, urllib.parse, json, sys

BASE = 'http://localhost:8000'

# 1) get token
try:
    data = urllib.parse.urlencode({
        'grant_type': 'password',
        'username': 'temp_admin',
        'password': 'TempPass123!',
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string',
    }).encode('utf-8')
    req = urllib.request.Request(f'{BASE}/auth/token', data=data, headers={'Content-Type':'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=10) as r:
        token_resp = json.load(r)
    access = token_resp.get('access_token')
    if not access:
        print('FAILED to obtain access_token', token_resp)
        sys.exit(2)
    print('Got access token')
except Exception as e:
    print('Token request failed:', e)
    sys.exit(2)

# 2) create ward
ward_payload = {'ward_name': 'E2E Ward', 'capacity': 3}
try:
    b = json.dumps(ward_payload).encode('utf-8')
    req = urllib.request.Request(f'{BASE}/wards', data=b, headers={'Content-Type':'application/json', 'Authorization': f'Bearer {access}'})
    with urllib.request.urlopen(req, timeout=10) as r:
        created = json.load(r)
    print('Created ward:', created)
except Exception as e:
    print('Create ward failed:', e)
    # print server response if available
    try:
        import http.client
    except Exception:
        pass
    sys.exit(3)

# 3) list wards
try:
    req = urllib.request.Request(f'{BASE}/wards', headers={'Authorization': f'Bearer {access}'})
    with urllib.request.urlopen(req, timeout=10) as r:
        wards = json.load(r)
    print('Wards list length:', len(wards))
    print('Last ward in list:', wards[-1] if wards else None)
except Exception as e:
    print('List wards failed:', e)
    sys.exit(4)

print('E2E test completed successfully')
