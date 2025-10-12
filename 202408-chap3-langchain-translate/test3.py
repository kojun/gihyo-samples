#!/usr/bin/env python

import httpx
r = httpx.get('https://www.asahi.com')
print(r.status_code)
