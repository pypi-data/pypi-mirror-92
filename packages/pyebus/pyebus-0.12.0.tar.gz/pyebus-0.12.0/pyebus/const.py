"""Constants."""


class _NotAvailable:

    """Not Available."""

    def __str__(self):
        return "Not Available"

    def __repr__(self):
        return "NA"


OK = "ok"
AUTO = "A"
NA = _NotAvailable()
