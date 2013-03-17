#!/usr/bin/env python
#-*- coding: utf8 -*-
"""
##########################################################################
 check_delegation_domain - Plugin for nagios to check date delegation domain names

 Copyright © 2009-2012 Denis 'Saymon21' Khabarov
 E-Mail: <saymon@hub21.ru>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License version 3
 as published by the Free Software Foundation.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
 Depends: http://pypi.python.org/pypi/whois/
 pip install whois 
"""

import datetime, argparse, sys
try: 
	import whois
except ImportError as errmsg:
	print >> sys.stderr, str(errmsg)
	print("For install module whois usage: pip install whois or apt-get install python-whois")
	sys.exit(3)

cliparser = argparse.ArgumentParser(prog=sys.argv[0],description='''Plugin for nagios to check date delegation domain names
ATTENTION! This is supports only zones: be, co, name, ru, de, jp, us, lv, me, nz, biz, uk, eu, org, net, com, pl
Copyright © 2009-2012 Denis 'Saymon21' Khabarov
E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)
Licence: GNU GPLv3''',epilog='''
Example usage: 
%(prog)s --domain=example.ru --warning=30 --critical=10''',
formatter_class=argparse.RawDescriptionHelpFormatter)
cliparser.add_argument("--domain", help="Domain, e.x example.com",required=True)
cliparser.add_argument("--warning",help="Warning days",required=True)
cliparser.add_argument("--critical",help="Critical days",required=True)
cliargs = cliparser.parse_args()

def main():
	domain = whois.query(cliargs.domain)
	if not domain:
		print "CRITICAL Couldn't resolve host "+cliargs.domain
		sys.exit(2)
		
	now_date = datetime.datetime.now()
	delta = domain.expiration_date - now_date
	expire_days=delta.days

	if expire_days <= int(cliargs.critical):
		print("CRITICAL Domain "+cliargs.domain+" expired in next "+str(expire_days)+" day(s)")
		sys.exit(2)
	elif expire_days <= int(cliargs.warning):
		print("WARNING Domain "+cliargs.domain+" expired in next "+str(expire_days)+" day(s)")
		sys.exit(1)
	else:
		print("OK Domain "+cliargs.domain+" expired in next "+str(expire_days)+" day(s)")
		sys.exit(0)

if __name__ == "__main__":
	main()
