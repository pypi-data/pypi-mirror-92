
import validators
from urllib.parse import urlparse
import datetime
import pytz
import uuid
from pathlib import Path
import mimetypes




class Email:
    def __init__(self, email = None):
        self.email = email
        self._domain = None
        self._valid = None

    @property
    def valid(self):
        """
        Validate an email format.

        Parameters
        ----------
        email (str): The email to validate

        Returns
        -------
        bool : True if valid, else false
        """

        
        self._valid = validators.email(self.email)
        return self._valid

    @property
    def domain(self):
        """
        Returns the domain of an email.

        Parameters
        ----------
        url (str): The email from which to get the domain

        Returns
        -------
        str : The domain of the email or None
        """

        # Error handling
        if not self.email:
            return None

        # Extract domain
        self._domain = self.email.split('@')[1]
        
        return self._domain
