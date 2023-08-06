"""
Celery configuration
https://docs.celeryproject.org/en/stable/userguide/configuration.html
"""

import conveyorbelt.celeryconfig_local

# Broker settings
# https://docs.celeryproject.org/en/stable/userguide/configuration.html#broker-settings
broker_url = conveyorbelt.celeryconfig_local.broker_url
