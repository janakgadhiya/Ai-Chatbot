from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.auth_db
users_collection = db.get_collection("users")

async def get_user(username: str):
    user = await users_collection.find_one({"username": username})
    return user