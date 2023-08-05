import httpx

HTTP = httpx.AsyncClient(http2=True)


class JsonSerializable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to JSON format.
    All subclasses of this class must override to_json.
    """

    def to_json(self):
        """
        Returns a JSON string representation of this class.
        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


def convert_markup(markup):
    if isinstance(markup, JsonSerializable):
        return markup.to_json()
    return markup
