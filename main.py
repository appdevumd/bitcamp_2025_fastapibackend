from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Middleware to allow all origins (for Flutter dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
# Get your MongoURL after creating your mongo atlas account and creating a new cluster
MONGO_URL = "" 
client = AsyncIOMotorClient(MONGO_URL)
db = client.travel
destination_collection = db.destinations

def serialize_destination(destination) -> dict:
    return {
        "id": str(destination["_id"]),
        "city": destination["city"],
        "country": destination["country"],
        "distance": destination["distance"],
        "cost": destination["cost"],
        "openingHours": destination["openingHours"],
        "image": destination["image"],
    }

@app.get("/api/get_all")
async def get_all_destinations():
    destinations_cursor = destination_collection.find()
    destinations = []
    async for dest in destinations_cursor:
        destinations.append(serialize_destination(dest))
    return destinations
