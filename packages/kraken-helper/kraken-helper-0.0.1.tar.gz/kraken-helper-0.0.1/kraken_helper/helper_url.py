import validators
from urllib.parse import urlparse
import datetime
import pytz
import uuid
from pathlib import Path
import mimetypes



class Url:
    def __init__(self, url = None):
        self.url = url
        self._domain = None
        self._valid = None

        self._ext = None
        self._name = None
        self._stem = None
        self._file_type = None

        self._parse()



    def _parse(self):

        #self._validate()

        self._parse_file()
        self._parse_domain()



    
    @property
    def valid(self, url = None):
        """
        Validate a url format.

        Parameters
        ----------
        url (str): The url to vlaidate

        Returns
        -------
        bool : True if valid, else false
        """

        if url:
            self.url = url
        
        # Error handling
        if not self.url:
            self.valid = False
            return self.valid

        # Perform validation
        self._valid = validators.url(url)

        return self.valid



    def _parse_domain(self):
        """
        Returns the domain of a url.

        Parameters
        ----------
        url (str): The url from which to get the domain

        Returns
        -------
        str : The domain of the url or None
        """

        # Error handling
        if not self.url:
            return None
    
        # Get the domain of an url
        
        parsed = urlparse(self.url)
        domain = parsed.netloc
        
        # Put domain in lowercase
        domain = domain.lower()

        domain = domain.replace('www.', '')
        
        self._domain = domain



    def _parse_file(self):
        
        self._ext = Path(self.url).suffix
        self._name = Path(self.url).name
        self._stem = Path(self.url).stem

    def _parse_type(self):
        self._file_type = mimetypes.guess_type(self.url)

    
    def valid(self, url = None):
        if url:
            self.url = url
            self._parse()

        return self.valid

    @property
    def domain(self, url = None):
        if url:
            self.url = url
            self._parse()
        return self._domain

    @property
    def type(self):
        return self.file_type

    @property
    def extension(self):

        return self.ext

    @property
    def name(self):

        return self.name

    @property
    def stem(self):

        return self.stem



