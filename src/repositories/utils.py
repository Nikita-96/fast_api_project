from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_free(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    query_1 = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_to >= date_from,
            BookingsOrm.date_from <= date_to
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="query_1")
    )
    query_2 = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(query_1.c.rooms_booked ,0)).label("free_rooms_count")

        )
        .select_from(RoomsOrm)
        .outerjoin(query_1, RoomsOrm.id == query_1.c.room_id)
        .cte(name="query_2")
    )

    sub_query = select(RoomsOrm.id).select_from(RoomsOrm)
    if hotel_id:
        sub_query = sub_query.filter_by(hotel_id=hotel_id)
    sub_query = sub_query.subquery(name="rooms_for_hotel")

    query_itog = (
        select(query_2.c.room_id)
        .select_from(query_2)
        .filter(
            query_2.c.free_rooms_count > 0,
            query_2.c.room_id.in_(sub_query)
        )
    )

    return query_itog