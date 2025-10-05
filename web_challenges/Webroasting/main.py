from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx
import hashlib
import asyncio  # for background task creation
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

MICROSERVICES: Dict[str, str] = {}

KERBEROS_CREDS = {
    "username": "admin",
    "password": "ADi$Secure_let1sbrIng1t0W3b!"
}

FLAG = "SecurinetsENIT{27186e6c7a5b39d5d864031dcbe95a7f}"


class ServiceRegistration(BaseModel):
    service_name: str
    service_url: str


def kerberos_hash(username: str, password: str) -> str:
    return hashlib.md5(f"{username}:{password}".encode()).hexdigest()


async def admin_bot_register(service_name: str, service_url: str) -> None:
    """
    Background coroutine that notifies the registered service with the admin
    credentials and their kerberos hash via POST to {service_url}/auth.
    Runs asynchronously (non-blocking).
    """
    admin_user = KERBEROS_CREDS["username"]
    admin_pwd = KERBEROS_CREDS["password"]
    admin_hash = kerberos_hash(admin_user, admin_pwd)

    auth_endpoint = f"{service_url.rstrip('/')}/auth"
    payload = {"username": admin_user, "kerberos_hash": admin_hash, "source": "admin-bot"}

    logger.info(f"[admin-bot] Attempting to register admin at {auth_endpoint} for service '{service_name}'")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(auth_endpoint, json=payload, timeout=5)
            if resp.status_code >= 200 and resp.status_code < 300:
                logger.info(f"[admin-bot] Admin successfully registered with {service_name} ({auth_endpoint})")
            else:
                logger.warning(
                    f"[admin-bot] Received non-2xx from {auth_endpoint} for {service_name}: {resp.status_code} - {resp.text}"
                )
    except httpx.RequestError as e:
        logger.error(f"[admin-bot] Network error while contacting {auth_endpoint} for {service_name}: {e}")
    except Exception as e:
        logger.exception(f"[admin-bot] Unexpected error while registering admin for {service_name}: {e}")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/register")
async def register_service(service: ServiceRegistration):
    if not service.service_name or not service.service_url:
        raise HTTPException(status_code=400, detail="Missing service_name or service_url")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(service.service_url, timeout=5)
            if response.status_code == 200:
                MICROSERVICES[service.service_name] = service.service_url
                logger.info(f"[+] Registered service: {service.service_name} -> {service.service_url}")

                # Trigger the admin-bot asynchronously (non-blocking).
                # We don't await it — it will run in the background.
                try:
                    asyncio.create_task(admin_bot_register(service.service_name, service.service_url))
                except RuntimeError:
                    # If there's no running loop (unlikely under uvicorn), schedule safe fallback:
                    logger.exception("[register_service] Failed to create background task with asyncio.create_task()")

                return {"message": f"Service {service.service_name} registered successfully"}
            else:
                raise HTTPException(status_code=400, detail="Service verification failed")
        except httpx.RequestError:
            raise HTTPException(status_code=400, detail="Invalid service URL")


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    hash_value = kerberos_hash(username, password)

    async with httpx.AsyncClient() as client:
        for service_name, service_url in MICROSERVICES.items():
            try:
                logger.info(f"[>] Sending creds to {service_url}/auth: {username} | hash: {hash_value}")
                await client.post(
                    f"{service_url.rstrip('/')}/auth",
                    json={"username": username, "kerberos_hash": hash_value},
                    timeout=5,
                )
            except httpx.RequestError:
                logger.warning(f"[!] Failed to reach {service_url}/auth")

    if username == KERBEROS_CREDS["username"] and password == KERBEROS_CREDS["password"]:
        return templates.TemplateResponse("flag.html", {"request": request, "flag": FLAG})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


@app.get("/admin", response_class=HTMLResponse)
async def admin_form(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse("admin.html", {"request": request, "error": error})


@app.post("/admin", response_class=HTMLResponse)
async def admin_access(request: Request, username: str = Form(...), provided_hash: str = Form(...)):
    expected_hash = kerberos_hash(KERBEROS_CREDS["username"], KERBEROS_CREDS["password"])
    if username == KERBEROS_CREDS["username"] and provided_hash == expected_hash:
        return templates.TemplateResponse("flag.html", {"request": request, "flag": FLAG})
    else:
        return templates.TemplateResponse("admin.html", {"request": request, "error": "Unauthorized"})
