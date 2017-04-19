# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems

# !/usr/bin/env python3

import requests
import json
import time
import datetime
import meraki_init
import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth

from meraki_init import MERAKI_API_KEY

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# The following declarations need to be updated based on your lab environment


