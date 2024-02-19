from bson import ObjectId
import pymongo

dbClient = pymongo.MongoClient('mongodb://localhost:27017/')
db = dbClient["hotel"]

roomTypes_collection = db['RoomTypes']
rooms_collection = db['Rooms']
user_collection = db['Users']
booking_collection = db['Bookings']
enquiry_collection = db['Enquiries']
payment_collection = db['payments']
feedback_collection = db['feedbacks']


def getRoomTypeById(id):
    query = {"_id": ObjectId(id)}
    return roomTypes_collection.find_one(query)

def getRoomById(id):
    query = {"_id": ObjectId(id)}
    return rooms_collection.find_one(query)

def getUserById(id):
    return user_collection.find_one({"_id": ObjectId(id)})