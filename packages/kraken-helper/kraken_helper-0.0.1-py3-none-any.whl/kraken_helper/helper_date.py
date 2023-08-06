


import validators
from urllib.parse import urlparse
import datetime
import pytz
import uuid
from pathlib import Path
import mimetypes




class Date:
    def _init__(self, input_date = None):
        self.date = input_date

    # Date handling functions
    @property
    def now(self):
        """
        Returns the current date in datetime format.

        Parameters
        ----------

        Returns
        -------
        datetime : The current datetime
        """

        # Returns current datetime 
        self.date = datetime.datetime.now(datetime.timezone.utc)
        return self.date

    def text(self, input_date):
        """
        Returns the date in human-readable date format.

        Parameters
        ----------
        input_date (datetime): The date to convert

        Returns
        -------
        str : The date in human format
        """


        self.text = input_date.strftime("%x")
        return self.text

    def date_to_datetime(self, value):

        return datetime.datetime.fromisoformat(value)