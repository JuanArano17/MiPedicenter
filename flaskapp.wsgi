#!/usr/bin/python
import sys
sys.path.insert(0, '/var/www/pedicenter')
from run import create_app
application = create_app()