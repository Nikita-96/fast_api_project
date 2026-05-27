from datetime import date

from src.schema.bookings import BookingsAdd

async def test_booking_add(db):
    user = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0].id
    booking_data = BookingsAdd(
        user_id=user,
        price=100,
        room_id=room,
        date_from=date(year=2025, month=12, day=12),
        date_to=date(year=2025, month=12, day=20),
    )
    new_booking = await db.bookings.add(booking_data)
    await db.commit()
    assert user == new_booking.user_id

async def test_booking_crud(db):
    user = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0].id
    booking_data = BookingsAdd(
        user_id=user,
        price=100,
        room_id=room,
        date_from=date(year=2025, month=12, day=12),
        date_to=date(year=2025, month=12, day=20),
    )

    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id

    update_date = date(year=2025, month=12, day=25)
    update_booking_data = BookingsAdd(
        user_id=user,
        price=100,
        room_id=room,
        date_from=date(year=2025, month=12, day=12),
        date_to=date(year=2025, month=12, day=25),
    )

    await db.bookings.edit(update_booking_data, id=new_booking.id)
    update_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert update_booking
    assert update_booking.id == new_booking.id
    assert update_booking.date_to == update_date

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
