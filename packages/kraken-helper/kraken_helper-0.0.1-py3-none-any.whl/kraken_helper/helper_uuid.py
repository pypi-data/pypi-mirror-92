

import validators
from urllib.parse import urlparse
import datetime
import pytz
import uuid
from pathlib import Path
import mimetypes



class UUID:
    def __init__(self):
        self.uuid = None
    
    
    def get(self):
        """
        Returns a random uuid.

        Parameters
        ----------

        Returns
        -------
        str : A random uuid
        """

        new_uuid = uuid.uuid4()
        self.uuid = str(new_uuid)
        return self.uuid
