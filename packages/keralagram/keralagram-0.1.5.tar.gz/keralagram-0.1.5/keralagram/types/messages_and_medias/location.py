import json


class Location(object):
    @classmethod
    def _de_json(cls, json_str: dict):
        if json_str is None:
            return None
        if isinstance(json_str, dict):
            json_obj = json_str
        elif isinstance(json_str, str):
            json_obj = json.loads(json_str)
        else:
            raise ValueError("Expected dict or str type")

        longitude = json_obj.get("longitude")
        latitude = json_obj.get("latitude")
        horizontal_accuracy = json_obj.get("horizontal_accuracy")
        live_period = json_obj.get("live_period")
        heading = json_obj.get("heading")
        proximity_alert_radius = json_obj.get("proximity_alert_radius")

        return cls(longitude, latitude, horizontal_accuracy, live_period, heading,
                   proximity_alert_radius)

    def __init__(self, longitude, latitude, horizontal_accuracy, live_period, heading,
                 proximity_alert_radius):
        self.longitude = longitude
        self.latitude = latitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius
