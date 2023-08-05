# coding=utf-8
from __future__ import unicode_literals

import json
import time


class Topic(object):
    MEDIUM = b"medium"  # alpr, nfc, command
    ACCESS_ACCEPT = b"access_accept"  # open
    ACCESS_REJECT = b"access_reject"  # e.g. if number plate is not found in database
    SENSOR = b"sensor"  # induction loop e.g for presence or counting
    COUNT = b"count"  # topic for the actual count how many vehicles are e.g. in the parking lot
    HEALTH = b"healthz"  # healthz checks
    IO = b"io"  # io events topic
    PAYMENT = b"payment"  # payment topic
    NOTICE = b"notice"  # topic for text/audio not
    GROUPING = b"grouping"  # topic for alpr grouping mechanism
    OPEN = b"ioopen"  # topic for permanently opening a gate
    PORTER = b"porter"  # topic for porter commands
    ALPR_RESULT = b"alpr_result"  # topic for sending alpr result to tracking
    TRACKING_COUNT = b"tracking_count"  # topic for tracking based counting
    TRACKING_DEBUG = b"tracking_debug"  # topic to trigger image save when new track
    BACKEND = b"backend"  # topic used for external authorization providers
    WEBAPP = b"webapp"  # topic used for webapp access
    TO_DISPLAY = b"to_display"  # show specific message on display
    ZONE = b"zone"
    SENTRY = b"sentry"  # report errors to sentry service
    PRESENCE = b"presence"
    GENERIC_LOG = b"generic_log"
    ALERT = b"alert"


class Message(dict):
    _MANDATORY_FIELDS = ["name", "type"]
    TIMESTAMP_ON_SERIALIZE = True

    @classmethod
    def parse(cls, msg):
        try:
            if hasattr(msg, "encode"):
                msg = msg.encode()
            parsed = json.loads(msg)
        except Exception as e:
            raise ValueError("Could not parse message")
        if not all(k in parsed for k in cls._MANDATORY_FIELDS):
            raise KeyError("Mandatory keys not found in message")
        return parsed

    @classmethod
    def serialize(cls, msg):
        if not isinstance(msg, dict):
            raise TypeError("Message is not of type dict")
        if not all(k in msg for k in cls._MANDATORY_FIELDS):
            raise KeyError("Mandatory keys not found in message")
        try:
            if Message.TIMESTAMP_ON_SERIALIZE:
                msg.update(timestamp=time.time())
            serialized = json.dumps(msg)
        except (TypeError, ValueError):
            raise ValueError("Could not serialize message")
        return serialized

    def __init__(self, name=None, type=None, *args, **kwargs):
        kwargs["type"] = type
        if "__prefix" in kwargs:
            kwargs["name"] = name
            del kwargs["__prefix"]
        else:
            kwargs["name"] = "{}-{}".format(type, name)
        super(Message, self).__init__(*args, **kwargs)

    def to_json(self):
        return Message.serialize(self)

    def from_json(self, serialized):
        self.clear()
        self.update(Message.parse(serialized))

    def to_socket(self, sock, topic):
        json_str = self.to_json()
        if hasattr(json_str, "encode"):
            json_str = json_str.encode("ascii")
        sock.send_multipart((topic, json_str))

    @classmethod
    def from_socket(cls, sock):
        topic, payload = sock.recv_multipart()
        # beware: __prefix=False will be supplied as kwargs parameter in the __init__ function
        message = cls(__prefix=False, **cls.parse(payload))
        return topic, message

    def set_gateway(self, gate, direction=None):
        gateway = dict(gate=(str(gate) or "unknown"),
                       direction=(str(direction) or ""))
        self.update(gateway=gateway)

    def is_gateway(self):
        return "gateway" in self

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)


def create_generic_log_msg(name, type, message, values, level, plate=None, gateway=None, transaction_id=None,
                           user=None, vehicle_id=None, source=None):
    """
    Generates a generic log message.

    Example:
        og = create_generic_log_msg(
            config.NAME, "open_gate", "Opened {{gate}} for {{medium}}", values={"gate": gate_name, "medium": medium.id},
            level="info", plate=medium.id, gateway={"gate": gate, "direction": direction}
        )

    :param name: name of current service
    :param type: message type
    :param message: text that will be presented in the event log
    :param values: values that will be inserted in the message
    :param level: error, info, warning, debug
    :param plate: any medium id
    :param gateway: gateway of the current service
    :param transaction_id: current parking session id
    :param user: current user
    :param vehicle_id: vehicle id (important for showing image)
    :param source: for images if gate != gate in ALPR
    :return:
    """
    msg = Message(name=name, type=type)
    msg["message"] = message
    msg["values"] = values
    msg["level"] = level
    if plate:
        msg["id"] = plate
    if gateway:
        msg["gateway"] = gateway
    if transaction_id:
        msg["transaction_id"] = transaction_id
    if user:
        msg["user"] = user
    if vehicle_id:
        msg["vehicle_id"] = vehicle_id
    if source:
        msg["source"] = source
    return msg
