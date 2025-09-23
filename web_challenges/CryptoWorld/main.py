from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
import secrets
import os

app = FastAPI(title="CryptoExchange API", description="CryptoExchange API you can use to interact with wallets and users.")

# In-memory storage
users_db = {}
wallets_db = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class User(BaseModel):
    username: str
    balance: float


class Wallet(BaseModel):
    owner_id: str
    balance: float
    currency: str
    FLAG:str


class TransferRequest(BaseModel):
    amount: float
    currency: str


def generate_id():
    return secrets.token_hex(8)


# Initialize data with flag
@app.on_event("startup")
async def startup():
    # Create users
    user1_id = generate_id()
    user2_id = generate_id()

    users_db[user1_id] = User(username="alice", balance=1000.0)
    users_db[user2_id] = User(username="bob", balance=500.0)

    # Create wallets
    wallet1_id = generate_id()
    wallet2_id = generate_id()
    wallet3_id = generate_id()
    wallet4_id = generate_id()

    # Store the flag in Bob's ETH wallet balance as a special value
    FLAG = "SecurinetsENIT{01c1ff55c322453ab1e016bf7dbc6537}"

    wallets_db[wallet1_id] = Wallet(owner_id=user1_id, balance=100.0, FLAG="none",currency="BTC")
    wallets_db[wallet2_id] = Wallet(owner_id=user1_id, balance=5000.0, FLAG="none",currency="ETH")
    wallets_db[wallet3_id] = Wallet(owner_id=user2_id, balance=50.0, FLAG="none",currency="BTC")
    wallets_db[wallet4_id] = Wallet(owner_id=user2_id, balance=500, FLAG=FLAG,currency="ETH")  # Flag here!

    print("=== This is the challenge  ===")
    print(f"Alice User ID: {user1_id}")
    print(f"Bob User ID: {user2_id}")
    print(f"Alice BTC Wallet ID: {wallet1_id}")
    print(f"Alice ETH Wallet ID: {wallet2_id}")
    print(f"Bob BTC Wallet ID: {wallet3_id}")
    print(f"Bob ETH Wallet ID: {wallet4_id} (Contains Flag!)")
    print("=================================")


def get_current_user_id():
    # Simulate authentication - Alice is always "authenticated"
    return list(users_db.keys())[0]


# --------- HTML PAGES ---------

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, "templates/index.html"))


@app.get("/debug", include_in_schema=False)
async def debug_page():
    return FileResponse(os.path.join(BASE_DIR, "templates/debug.html"))


@app.get("/api/docs", include_in_schema=False)
async def custom_docs():
    return FileResponse(os.path.join(BASE_DIR, "templates/docs.html"))


# --------- API ENDPOINTS ---------

@app.get("/api/user/{user_id}", summary="Get user information", description="Retrieve user details by user ID")
async def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.get("/api/wallets", summary="Get authenticated user's wallets",
         description="Returns wallets belonging to the currently authenticated user")
async def get_my_wallets(current_user_id: str = Depends(get_current_user_id)):
    my_wallets = []
    for wallet_id, wallet in wallets_db.items():
        if wallet.owner_id == current_user_id:
            my_wallets.append({"id": wallet_id, **wallet.dict()})
    return {"wallets": my_wallets}


@app.get("/api/user/{user_id}/wallets", summary="Get wallets by user ID",
         description="Retrieve all wallets belonging to a specific user")
async def get_user_wallets(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_wallets = []
    for wallet_id, wallet in wallets_db.items():
        if wallet.owner_id == user_id:
            user_wallets.append({"id": wallet_id, **wallet.dict()})
    return {"wallets": user_wallets}


@app.post("/api/wallet/{wallet_id}/transfer", summary="Transfer funds",
          description="Transfer funds from a wallet (requires ownership)")
async def transfer_funds(wallet_id: str, transfer: TransferRequest,
                         current_user_id: str = Depends(get_current_user_id)):
    if wallet_id not in wallets_db:
        raise HTTPException(status_code=404, detail="Wallet not found")

    wallet = wallets_db[wallet_id]

    if wallet.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if isinstance(wallet.balance, str):  # Flag wallet
        raise HTTPException(status_code=400, detail="Cannot transfer from this wallet")

    if wallet.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= transfer.amount
    return {"message": "Transfer successful", "new_balance": wallet.balance}


@app.get("/api/wallet/{wallet_id}", summary="Get wallet information",
         description="Retrieve wallet details by wallet ID")
async def get_wallet(wallet_id: str, current_user_id: str = Depends(get_current_user_id)):
    if wallet_id not in wallets_db:
        raise HTTPException(status_code=404, detail="Wallet not found")

    wallet = wallets_db[wallet_id]

    # VULNERABLE ENDPOINT: No ownership check!
    # This is where the BOLA vulnerability exists
    return wallet


@app.get("/api/debug", summary="Debug Information", description="Get all user and wallet IDs for testing purposes",
         include_in_schema=True)
async def debug_info():
    """Debug endpoint to help players understand the data structure"""
    alice_id = list(users_db.keys())[0]
    bob_id = list(users_db.keys())[1]

    # Find Bob's ETH wallet (the one with the flag)
    bob_eth_wallet_id = None
    for wallet_id, wallet in wallets_db.items():
        if wallet.owner_id == bob_id and wallet.currency == "ETH":
            bob_eth_wallet_id = wallet_id
            break

    return {
        "note": "This is a debugging endpoint. Do not use it in production",
        "hint": "Check the /api/wallet/{wallet_id} endpoint carefully...",
        "current_authenticated_user": {
            "id": alice_id,
            "username": users_db[alice_id].username
        },
        "bob_user": {
            "id": bob_id,
            "username": users_db[bob_id].username
        },
        "bob_eth_wallet_id": bob_eth_wallet_id,
        "total_users": len(users_db),
        "total_wallets": len(wallets_db)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
