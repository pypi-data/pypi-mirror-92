import fnmatch
import six


class Filter(dict):
    _RESERVED_KEYS = [
        "_name", "topic",
    ]
    RESERVED_KEYS = []
    REQUIRED_KEYS = []

    def __init__(self, **data):
        super(Filter, self).__init__(**data)
        for key in self.REQUIRED_KEYS:
            assert key in self

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __ne__(self, other):
        if other is None:
            return True
        return self.name != other.name

    def _strip_wildcard(self, topic):
        for char in ["*", "?", "[", "]"]:
            topic = topic.replace(char, "")
        return topic

    def _match_dict(self, message, data):
        for filter_key, filter_value in data.items():
            if filter_key in self._RESERVED_KEYS + self.RESERVED_KEYS:
                continue

            if filter_key not in message:
                return False

            inverted = isinstance(filter_value, (six.string_types)) and filter_value[0] == "!"
            if inverted:
                filter_value = filter_value[1:]

            message_value = message.get(filter_key)

            if isinstance(filter_value, dict):
                if not self._match_dict(message_value, filter_value):
                    return False
            elif isinstance(filter_value, (list, tuple)):
                if message_value not in filter_value:
                    return False
            elif inverted and message_value == filter_value:
                return False
            elif not inverted and message_value != filter_value:
                return False
        return True

    def subscribe(self, socket):
        if "topic" in self:
            socket.subscribe(self._strip_wildcard(self["topic"]).encode("ascii"))

    def match(self, topic, message):
        if hasattr(topic, "decode"):
            topic = topic.decode("ascii")
        if "topic" in self and (topic == self["topic"] or fnmatch.fnmatch(topic, self["topic"])):
            return self._match_dict(message, self)
        else:
            return False

    @property
    def name(self):
        return self.get("_name") or self.get("name")

    @property
    def topic(self):
        return self.get("topic")
