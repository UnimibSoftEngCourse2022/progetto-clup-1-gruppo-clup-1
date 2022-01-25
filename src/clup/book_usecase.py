import uuid

def book(market_id, queue):
    reservation_id = uuid.uuid1()
    reservation = (reservation_id, market_id)
    updated_queue = queue + (reservation_id,)
    return reservation, updated_queue
