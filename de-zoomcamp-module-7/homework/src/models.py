import json
from dataclasses import dataclass


@dataclass
class GreenRide:
    PULocationID: int
    DOLocationID: int
    trip_distance: float
    total_amount: float
    lpep_pickup_datetime: int


def ride_deserializer(data):
    json_str = data.decode("utf-8")
    ride_dict = json.loads(json_str)
    return GreenRide(**ride_dict)