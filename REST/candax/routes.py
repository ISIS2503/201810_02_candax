    # -*- coding: iso-8859-15 -*-

"""
routes
======

This module establishes and defines the Web Handlers and Websockets
that are associated with a specific URL routing name. New routing
associations must be defined here.

Notes
-----
For more information regarding routing URL and valid regular expressions
visit: http://www.tornadoweb.org/en/stable/guide/structure.html
"""

import os
import sys
import candax.web as web
import candax.rest.alarms_rest as alarms_rest
import candax.rest.residential_units_rest as residential_units_rest
import candax.rest.houses_rest as houses_rest
import candax.rest.locks_rest as locks_rest
import candax.rest.hubs_rest as hubs_rest
import candax.rest.alarms_owner_rest as alarms_owner_rest
import candax.rest.alarms_admin_rest as alarms_admin_rest
import candax.rest.administrators_rest as administrators_rest
import candax.rest.owners_rest as owners_rest
import candax.rest.passwordsMQTT_rest as passwordsMQTT_rest
import candax.rest.passwordsREST_rest as passwordsREST_rest
import candax.rest.yale_rest as yale_rest
import candax.rest.private_security_rest as private_security_rest
import candax.rest.auth_rest as auth_rest
import candax.rest.alarms_neighborhood_rest as alarms_neighborhood_rest
import candax.rest.realTime_residential_units_rest as realTime_residential_units_rest
import candax.rest.realTime_houses_rest as realTime_houses_rest
import candax.rest.month_residential_units_rest as month_residential_units_rest
import candax.rest.month_houses_rest as month_houses_rest
import candax.rest.alarms_silence_rest as alarms_silence_rest
import candax.rest.tree_rest as tree_rest
import candax.rest.houses_detail_rest as house_detail_rest
import candax.rest.ws as ws
import candax.rest.ws_alarms as ws_alarms

# import candax.rest as rest

# Define new rest associations
REST = [
    (r'/alarms(/?(.+)?)', alarms_rest.MainHandler), # YALE
    (r'/residentialUnits(/?(.+)?)', residential_units_rest.MainHandler),
    (r'/houses(/?(.+)?)', houses_rest.MainHandler),
    (r'/yale(/?(.+)?)', yale_rest.MainHandler),
    (r'/privateSecurity(/?(.+)?)', private_security_rest.MainHandler),
    (r'/hubs(/?(.+)?)', hubs_rest.MainHandler),
    (r'/locks(/?(.+)?)', locks_rest.MainHandler),
    (r'/owners(/?(.+)?)', owners_rest.MainHandler),
    (r'/administrators(/?(.+)?)', administrators_rest.MainHandler),
    (r'/history/owners/?(.+)?', alarms_owner_rest.MainHandler), #Propietario
    (r'/history/administrators/?(.+)?', alarms_admin_rest.MainHandler), #Admin
    (r'/passwords(/?(.+)?)', passwordsREST_rest.MainHandler),  #YALE
    (r'/publishPasswords(/?(.+)?)', passwordsMQTT_rest.MainHandler),  #YALE
    (r'/auth(/?(.+)?)', auth_rest.MainHandler),
    (r'/history/neighborhood/?(.+)?', alarms_neighborhood_rest.MainHandler),
    (r'/realTime/residentialUnit/?(.+)?', realTime_residential_units_rest.MainHandler),
    (r'/realTime/houses/?(.+)?', realTime_houses_rest.MainHandler),
    (r'/month/residentialUnit/?(.+)?', month_residential_units_rest.MainHandler),
    (r'/month/houses/?(.+)?', month_houses_rest.MainHandler),
    (r'/silence(/?(.+)?)', alarms_silence_rest.MainHandler),
    (r'/tree(/?(.+)?)', tree_rest.MainHandler),
    (r'/house_detail(/?(.+)?)', house_detail_rest.MainHandler),
    (r'/socket', ws.SocketHandler),
    (r'/socketAlarms', ws_alarms.SocketHandler)
]

# Define new web rendering route associations
WEB = [
    (r'/flights', web.flights_handler.MainHandler)
]

ROUTES = REST + WEB
