#!/usr/bin/python
import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.dirname(__file__))
from python import app as application
