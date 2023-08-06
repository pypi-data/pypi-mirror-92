
from kraken_helper.helper_url import Url
from kraken_helper.helper_uuid import UUID
from kraken_helper.helper_email import Email
from kraken_helper.helper_date import Date


class Kraken_helper:

    def __init__(self):

        a=1

    def domain(self, value):
        # Return the domain of a url or email
        
        # try email first
        
        e = Email(value)
        if e.valid:
            return e.domain

        # Try url
        u = Url(value)
        if u.valid:
            return u.domain

        return None


    @property
    def uuid(self):
        # Return a uuid

        u = UUID()
        return u.get()

    @property
    def now(self):
        # Gives current datetime

        d = Date()
        return d.now()


    def datetime_to_date(self, value):
        # COnvert datetime to date format

        d = Date()
        return d.text(value)


    def date_to_datetime(self, value):
        # Convert date 2011-01-23 to datetime format

        d = Date()

        return d.date_to_datetime(value)

