from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)
db = client[DATABASE_NAME]