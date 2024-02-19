from datetime import datetime
from bson import ObjectId
from app import app
from flask import flash, jsonify, redirect, render_template, request, session, url_for
from app import conn

@app.route("/")
def index():
    rooms = conn.rooms_collection.find()
    return render_template("public/index.html", rooms=rooms)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("public/register.html")
    else:
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        phone_number = request.form.get('phoneNumber')
        password = request.form.get('password')

        values = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "password": password
        }
        conn.user_collection.insert_one(values)
        flash("Registered successully, please login to book rooms", "success")
        return redirect(request.url)


@app.route("/is-email-exist", methods=["GET"])
def is_email_exist():
    email = request.args.get("email")
    user = conn.user_collection.find_one({"email": email})
    if user == None:
        return jsonify(True)
    else:
        return jsonify(False)



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("public/login.html", msg="")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        if password == 'admin' and email == 'admin@gmail.com':
            session['login'] = True
            session['role'] = "admin"
            return redirect("/admin/room-types")
        else:
            filter = {"email": email, "password": password}
            count = conn.user_collection.count_documents(filter)
            if count > 0:
                user = conn.user_collection.find_one(filter)
                session['login'] = True
                session['role'] = "customer"
                session['userId'] = str(user['_id'])
                session['userName'] = user['first_name']+" "+user['last_name']
                return redirect(url_for("index"))

    return render_template("public/login.html", msg="Invalid Login Credentials")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/change-password",methods=["GET","POST"])
def changePassword():
    if request.method == "POST":
        password = request.form.get("password")
        userId=session["userId"]
        conn.user_collection.update_one({"_id": ObjectId(userId)}, {
                '$set': {"password": password}})
        flash("Password updated successfully", "success")

    return render_template("public/changePassword.html")


@app.route("/filter-rooms")
def view_rooms():
    check_in_date = request.args.get("check_in_date")
    check_out_date = request.args.get("check_out_date")
    guests = request.args.get("guests")
    rooms = conn.rooms_collection.find({"guestCapacity":{'$gte':int(guests)}})
    return render_template("public/rooms.html", rooms=rooms,check_in_date=check_in_date,check_out_date=check_out_date,guests=guests)


@app.route("/room-details")
def room_details():
    roomId = request.args.get("roomId")
    room = conn.rooms_collection.find_one({"_id":ObjectId(roomId)})
    roomType = conn.getRoomTypeById(room['roomTypeId'])
    return render_template("public/room-details.html", room=room, roomType=roomType)


@app.route("/check-availabiity", methods=['POST'])
def check_availability():
    roomId = ObjectId(request.form.get("roomId"))
    room = conn.rooms_collection.find_one({"_id":roomId})
    roomType = conn.roomTypes_collection.find_one({"_id":room["roomTypeId"]})
    check_in_date = request.form.get("check_in_date")
    check_out_date = request.form.get("check_out_date") 
    check_in_date = datetime(
        *[int(v) for v in check_in_date.replace('T', '-').replace(':', '-').split('-')])
    check_out_date = datetime(
        *[int(v) for v in check_out_date.replace('T', '-').replace(':', '-').split('-')])    
    
    if checkReserved(check_in_date, check_out_date, roomId):
        flash("Sorry!, Room already booked in the above days try to book after that days ", "danger")
        return redirect(url_for("room_details",roomId=roomId))

    difference = check_out_date - check_in_date
    nights = difference.days
    totalAmount = float(room["pricePerNight"] * nights)

    guests = request.form.get("guests")

    return render_template("public/booking-confirmation.html",room=room,roomType=roomType, check_in_date=check_in_date, check_out_date=check_out_date,nights=nights,totalAmount=totalAmount,guests=guests)


@app.route("/bookroom",methods=["POST"])
def bookroom():
    roomId = request.form.get("roomId")
    check_in_date = request.form.get("check_in_date")
    check_in_date = datetime.strptime(check_in_date,"%Y-%m-%d %H:%M:%S")
    check_out_date = request.form.get("check_out_date")
    check_out_date = datetime.strptime(check_out_date,"%Y-%m-%d %H:%M:%S")
    nights = request.form.get("nights") 
    pricePerNight = request.form.get("pricePerNight") 
    totalAmount = request.form.get("totalAmount")
    bookedOn = datetime.utcnow()

    values={
        "bookedOn":bookedOn,
        "userId":ObjectId(session['userId']),
        "roomId":ObjectId(roomId),
        "check_in_date":check_in_date,
        "check_out_date":check_out_date,
        "nights":int(nights),
        "pricePerNight":float(pricePerNight),
        "totalAmount":float(totalAmount),
        "status":"Booked",
        "depositAmount":0
    }
    conn.booking_collection.insert_one(values)

    #payment details
    cardNumber = request.form.get("cardNumber")
    nameOnCard = request.form.get("nameOnCard")
    values = {
        "cardNumber":cardNumber,
        "nameOnCard":nameOnCard,
        "paymentStatus":"Success"
    }
    conn.payment_collection.insert_one(values)
    return redirect(url_for("view_bookings"))


@app.route("/bookings")
def view_bookings():
    userId=ObjectId(session['userId'])
    bookings = conn.booking_collection.find({"userId":userId})
    bookings = list(bookings)
    bookings.reverse()
    return render_template("/public/bookings.html", bookings=bookings,getRoomById=conn.getRoomById,getRoomTypeById=conn.getRoomTypeById)

    
def checkReserved(fromDate, toDate, roomId):
    query = {"roomId": ObjectId(roomId), "status": "Booked"}
    Bookings = conn.booking_collection.find(query)
    for Booking in Bookings:
        print("inside")
        fromDateBooked = Booking['check_in_date']
        toDateBooked = Booking['check_out_date']
        if fromDate >= fromDateBooked and fromDate <= toDateBooked:
            flash(f"Reserved From: {fromDateBooked.strftime('%Y-%m-%d')}  |  To: {toDateBooked.strftime('%Y-%m-%d')}")
            return True
        elif toDate >= fromDateBooked and toDate <= toDateBooked:
            flash(f"Reserved From: {fromDateBooked.strftime('%Y-%m-%d')}  |  To: {toDateBooked.strftime('%Y-%m-%d')}")
            return True
        elif fromDate < fromDateBooked and toDate > toDateBooked:
            flash(f"Reserved From: {fromDateBooked.strftime('%Y-%m-%d')}  |  To: {toDateBooked.strftime('%Y-%m-%d')}")
            return True
        print(fromDate >= fromDateBooked)
    return False


@app.route("/cancel")
def cancel_booking():
    bookingId=ObjectId(request.args.get("bookingId"))
    conn.booking_collection.update_one({"_id": ObjectId(bookingId)}, {
                '$set': {"status": "Cancelled"}})
    flash("Booking cancelled successully", "success")
    return redirect(url_for("view_bookings"))


@app.route("/queries",methods=["GET","POST"])
def enquiries():
    userId = ObjectId(session["userId"])
    enquiries = conn.enquiry_collection.find({"userId":userId})
    
    if request.method == "POST":
        query = request.form.get("query")
        conn.enquiry_collection.insert_one({"userId":userId,"query":query})
        flash("Query posted successfully", "success")
        return redirect(url_for("enquiries"))
    
    return render_template("/public/queries.html", enquiries=enquiries)


@app.route("/add-feedback", methods=["GET","POST"])
def add_feedbacks():
    roomId = request.args.get("roomId")
    if request.method == "POST":
        userId = ObjectId(session['userId'])
        roomId = request.form.get("roomId")
        feedback = request.form.get("feedback")
        values = {
            "userId":userId,
            "roomId":ObjectId(roomId),
            "feedback":feedback,
            "postedOn":datetime.utcnow()
        }
        conn.feedback_collection.insert_one(values)
        flash("Feedback posted successfully", "success")
        return redirect(url_for("add_feedbacks",roomId=roomId))

    return render_template("/public/add-feedback.html",roomId=roomId)


@app.route("/feedbacks")
def feedbacks():
    roomId = ObjectId(request.args.get("roomId"))
    feedbacks = conn.feedback_collection.find({"roomId":roomId})
    feedbacks = list(feedbacks)
    feedbacks.reverse()
    return render_template("/public/feedbacks.html",feedbacks=feedbacks,getUserById=conn.getUserById)
    
