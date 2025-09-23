from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import secrets
import os

app = FastAPI(title="CryptoExchange API", description="CryptoExchange API with authentication & BOFLA vulnerability")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------- In-Memory DB ---------
users_db = {}
wallets_db = {}
auth_tokens = {}  # token -> user_id


class User(BaseModel):
    username: str
    balance: float
    role: str = "user"  # user/admin


class Wallet(BaseModel):
    owner_id: str
    balance: float
    currency: str
    FLAG: str


class TransferRequest(BaseModel):
    amount: float
    currency: str


class LoginRequest(BaseModel):
    username: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --------- Utilities ---------
def generate_id():
    return secrets.token_hex(8)


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    if token not in auth_tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    return auth_tokens[token]


# --------- Startup (Init Data) ---------
@app.on_event("startup")
async def startup():
    # Users
    mohamed_id = generate_id()
    Kamel_id = generate_id()
    users_db[mohamed_id] = User(username="Mohamed", balance=1000, role="user")
    users_db[Kamel_id] = User(username="Kamel", balance=500, role="user")

    # Wallets
    wallet1_id = generate_id()
    wallet2_id = generate_id()
    wallet3_id = generate_id()
    wallet4_id = generate_id()

    FLAG = "SecurinetsENIT{cf2aab851361e65d9ef5d7c0415136cb}"

    wallets_db[wallet1_id] = Wallet(owner_id=mohamed_id, balance=100, FLAG="none", currency="BTC")
    wallets_db[wallet2_id] = Wallet(owner_id=mohamed_id, balance=5000, FLAG="none", currency="ETH")
    wallets_db[wallet3_id] = Wallet(owner_id=Kamel_id, balance=50, FLAG="none", currency="BTC")
    wallets_db[wallet4_id] = Wallet(owner_id=Kamel_id, balance=500, FLAG=FLAG, currency="ETH")

    print("=== Challenge Initialized ===")
    print(f"mohamed ID: {mohamed_id}, Kamel ID: {Kamel_id}")
    print(f"mohamed BTC: {wallet1_id}, mohamed ETH: {wallet2_id}")
    print(f"Kamel BTC: {wallet3_id}, Kamel ETH (FLAG!): {wallet4_id}")
    print("==============================")


# --------- Authentication ---------
@app.post("/api/login")
async def login(login: LoginRequest):
    # Find user by username
    for user_id, user in users_db.items():
        if user.username == login.username:
            # Generate token
            token = secrets.token_hex(16)
            auth_tokens[token] = user_id
            return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=404, detail="User not found")


# --------- HTML Pages ---------
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
@app.get("/api/user/{user_id}")
async def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.get("/api/wallets")
async def get_my_wallets(current_user_id: str = Depends(get_current_user_id)):
    my_wallets = []
    for wallet_id, wallet in wallets_db.items():
        if wallet.owner_id == current_user_id:
            my_wallets.append({"id": wallet_id, **wallet.dict()})
    return {"wallets": my_wallets}


@app.post("/api/wallet/{wallet_id}/transfer")
async def transfer_funds(wallet_id: str, transfer: TransferRequest,
                         current_user_id: str = Depends(get_current_user_id)):
    if wallet_id not in wallets_db:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet = wallets_db[wallet_id]
    if wallet.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    if isinstance(wallet.balance, str):
        raise HTTPException(status_code=400, detail="Cannot transfer from this wallet")
    if wallet.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    wallet.balance -= transfer.amount
    return {"message": "Transfer successful", "new_balance": wallet.balance}


# --------- Vulnerable Admin Function (BOFLA) ---------
@app.post("/api/admin/transfer_admin/{wallet_id}")
async def admin_transfer_vuln(wallet_id: str, transfer: TransferRequest,
                              current_user_id: str = Depends(get_current_user_id)):
    """
    Intended admin-only function.
    Vulnerability: No role check -> any authenticated user can call it.
    Returns FLAG if wallet contains it.
    """
    wallet = wallets_db.get(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.FLAG != "none":
        return {"flag": wallet.FLAG}
    if wallet.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    wallet.balance -= transfer.amount
    return {"message": "Transfer successful", "new_balance": wallet.balance}


# --------- Debug ---------
@app.get("/api/debug")
async def debug_info():
    mohamed_id = list(users_db.keys())[0]
    Kamel_id = list(users_db.keys())[1]

    Kamel_eth_wallet_id = None
    for wallet_id, wallet in wallets_db.items():
        if wallet.owner_id == Kamel_id and wallet.currency == "ETH":
            Kamel_eth_wallet_id = wallet_id
            break

    return {
        "note": "This is a Debug endpoint remove it in production",
        "hint": "You can't solve this challenge we added authentication",
        "current_authenticated_user": {"id": mohamed_id, "username": users_db[mohamed_id].username},
        "Kamel_user": {"id": Kamel_id, "username": users_db[Kamel_id].username},
        "Kamel_eth_wallet_id": Kamel_eth_wallet_id,
        "total_users": len(users_db),
        "total_wallets": len(wallets_db)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
