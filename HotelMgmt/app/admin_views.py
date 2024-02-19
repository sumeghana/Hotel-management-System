from app import app
from flask import flash, render_template, request, redirect, url_for
from app import conn
from bson import ObjectId
from app import APP_ROOT
import os


@app.route("/admin/")
def admin_index():
    return render_template("/admin/index.html")


@app.route("/admin/room-types", methods=["GET", "POST"])
def admin_roomtypes():
    if request.method == "POST":
        roomType = request.form.get('roomType')
        roomTypeId = request.form.get('roomTypeId')

        if roomType != None:
            query = {"roomType": roomType}
            count = conn.roomTypes_collection.count_documents(query)
            if count != 0:
                flash("This room type already exist", "warning")
                return redirect(request.url)

        if roomTypeId != "":
            conn.roomTypes_collection.update_one({"_id": ObjectId(roomTypeId)}, {
                '$set': {"roomType": roomType}})
            flash("Room type updated successully", "success")
        else:
            conn.roomTypes_collection.insert_one(
                {"roomType": roomType, "availability": True})
            flash("Room type added successully", "success")

        return redirect(request.url)
    else:
        roomTypeId = ObjectId(request.args.get("roomTypeId"))
        if roomTypeId != None:
            roomType = conn.roomTypes_collection.find_one({"_id": roomTypeId})

        roomTypes = conn.roomTypes_collection.find()
        roomTypes = list(roomTypes)
        list.reverse(roomTypes)
        return render_template("admin/room-types.html", roomTypes=roomTypes, roomType=roomType)


@app.route("/admin/rooms")
def admin_view_rooms():
    rooms = conn.rooms_collection.find()
    rooms = list(rooms)
    list.reverse(rooms)
    return render_template("admin/rooms.html", rooms=rooms, getRoomTypeById=conn.getRoomTypeById)


@app.route("/admin/add-room", methods=["GET", "POST"])
def admin_add_room():
    roomTypes = conn.roomTypes_collection.find()
    if request.method == "POST":
      req = request.form
      roomTypeId = req.get("roomTypeId")
      roomNo = req.get("roomNo")
      guestCapacity = req.get("guestCapacity")
      bedType = req.get("bedType")
      pricePerNight = req.get("pricePerNight")
      amenities = req.get("amenities")
      roomImage = request.files.get('roomImage')
      roomImage.save(APP_ROOT+"/uploads/"+roomImage.filename)

      query = {
          "roomTypeId": ObjectId(roomTypeId),
          "roomNo": roomNo,
          "bedType": bedType,
          "guestCapacity": int(guestCapacity),
          "pricePerNight": float(pricePerNight),
          "roomImagePath": roomImage.filename,
          "amenities": amenities,
          "roomStatus": True
      }
      conn.rooms_collection.insert_one(query)
      return redirect(url_for("admin_view_rooms"))
    else:
      return render_template("admin/room-save.html", roomTypes=roomTypes, room="")


@app.route("/admin/edit-room", methods=["GET", "POST"])
def admin_edit_room():
    roomTypes = conn.roomTypes_collection.find()
    if request.method == "POST":
      req = request.form
      roomId = ObjectId(req.get("roomId"))
      roomTypeId = req.get("roomTypeId")
      roomNo = req.get("roomNo")
      guestCapacity = req.get("guestCapacity")
      bedType = req.get("bedType")
      pricePerNight = req.get("pricePerNight")
      amenities = req.get("amenities")
      roomImagePath = req.get('oldImagePath')

      if request.files['roomImage'].filename != '':
        picture = request.files.get('roomImage')
        picture.save(APP_ROOT+"/uploads/"+picture.filename)
        os.remove(APP_ROOT+"/uploads/"+request.form.get('oldImagePath'))
        roomImagePath = picture.filename

      values = {
          "roomTypeId": ObjectId(roomTypeId),
          "bedType": bedType,
          "roomNo": roomNo,
          "guestCapacity": int(guestCapacity),
          "pricePerNight": float(pricePerNight),
          "roomImagePath": roomImagePath,
          "amenities": amenities,
          "roomStatus": True
      }
      conn.rooms_collection.update_one({'_id': roomId}, {
          '$set': values})
      return redirect(url_for("admin_view_rooms"))
    else:
        roomId = ObjectId(request.args.get("roomId"))
        room = conn.rooms_collection.find_one({'_id': roomId})
        return render_template("admin/room-save.html", roomTypes=roomTypes, room=room)


@app.route("/admin/bookings")
def admin_view_bookings():
    bookings = conn.booking_collection.find()
    bookings = list(bookings)
    list.reverse(bookings)
    return render_template("admin/bookings.html", bookings=bookings,getUserById=conn.getUserById, getRoomById=conn.getRoomById)

@app.route("/admin/availability")
def admin_view_availability():
    availability = conn.booking_collection.find()
    availability = list(availability)
    list.reverse(availability)
    return render_template("admin/avail.html", bookings=availability,getUserById=conn.getUserById, getRoomById=conn.getRoomById)
@app.route("/admin/check")
def admin_view_check():
    check = conn.booking_collection.find()
    check = list(check)
    list.reverse(check)
    return render_template("admin/checkin.html", bookings=check,getUserById=conn.getUserById, getRoomById=conn.getRoomById)

@app.route("/admin/cancel")
def admin_cancel_booking():
    bookingId=ObjectId(request.args.get("bookingId"))
    conn.booking_collection.update_one({"_id": ObjectId(bookingId)}, {
                '$set': {"status": "Cancelled"}})
    flash("Booking cancelled successully", "success")
    return redirect(url_for("admin_view_bookings"))

@app.route("/admin/checkin")
def admin_checkin():
    bookingId=ObjectId(request.args.get("bookingId"))
    depositAmount=request.args.get("depositAmount")
    ##flash('depositAmount',depositAmount)
    ##flash(request.args)
    conn.booking_collection.update_one({"_id": ObjectId(bookingId)}, {
                '$set': {"depositAmount": depositAmount}})
    flash("Check-In Compleated successully", "success")
    return redirect(url_for("admin_view_check"))

@app.route("/admin/checkout")
def admin_checkout():
    bookingId=ObjectId(request.args.get("bookingId"))
    charges=request.args.get("charges")
    bookings = conn.booking_collection.find_one({"_id": ObjectId(bookingId)})
    depositAmount = bookings["depositAmount"]
    x=int(depositAmount)-int(charges)
    if x>0:
        flash("Please Return the Change $"+ str(x),"success")
    else:
        flash("please collect the Amount $"+str(abs(x)),"success")
    flash("Check-Out Compleated successully", "success")
    conn.booking_collection.update_one({"_id": ObjectId(bookingId)}, {
                '$set': {"status": "Cancelled"}})
    return redirect(url_for("admin_view_check"))

@app.route("/admin/enquiries")
def admin_enquiries():
    enquiries = conn.enquiry_collection.find()
    return render_template("admin/enquiries.html",enquiries=enquiries,getUserById=conn.getUserById)


@app.route("/admin/query-response", methods=["GET","POST"])
def admin_query_response():
    enquiryId=ObjectId(request.args.get("enquiryId"))
    enquiry = conn.enquiry_collection.find_one({"_id":enquiryId})
    if request.method == "POST":
        enquiryId = request.form.get("enquiryId")
        response = request.form.get("response")
        conn.enquiry_collection.update_one({"_id": ObjectId(enquiryId)}, {
                '$set': {"response": response}})
        flash("Response updated successully", "success")
        return redirect(url_for("admin_enquiries"))
    
    return render_template("admin/query-response.html",enquiry=enquiry)

@app.route("/admin/feedbacks")
def admin_feedbacks():
    roomId = ObjectId(request.args.get("roomId"))
    feedbacks = conn.feedback_collection.find({"roomId":roomId})
    feedbacks = list(feedbacks)
    feedbacks.reverse()
    return render_template("admin/feedbacks.html",feedbacks=feedbacks,getUserById=conn.getUserById)






