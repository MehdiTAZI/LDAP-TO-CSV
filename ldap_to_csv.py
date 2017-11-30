#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from optparse import OptionParser
import ldap
import sys


def eprint(*args, **kwargs):
    print(file=sys.stderr, *args, **kwargs)


def getEntryFromDN(ldap_instance, basedn):
    try:
        retrieveAttributes = None
        searchFilter = 'cn=*'
        ldap_result_id = ldap_instance.search_s(basedn,
                ldap.SCOPE_SUBTREE, 'cn=*', retrieveAttributes)
        return ldap_result_id
    except ldap.LDAPError, e:
        return False


def saveElemsToCSVFile(entries, headerKeyLabel, filename):

    headers = [headerKeyLabel]

    for entry in entries:
        for (key, elem) in entry[1].items():
            if key not in headers:
                headers.append(key)

    with open(filename, 'wb') as file:
        file.write(columns_separator.join(headers))
        file.write(line_separator)

        count = 0
        for entry in entries:

            row = {}

            if count > 0:
                file.write(line_separator)

            count = count + 1
            row[headerKeyLabel] = entry[0]

            for (key, elem) in entry[1].items():
                if key in row:
                    row[key].append(value_elems_separator.join(elem))
                else:
                    row[key] = value_elems_separator.join(elem)

            for header_key in headers:
                if header_key in row:
                    file.write(row.get(header_key))
                file.write(columns_separator)


def initLDAP(
    ldap_server_url,
    ldap_server_login,
    ldap_server_password,
    certif_filename,
    ):
    try:

        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, certif_filename)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,
                        ldap.OPT_X_TLS_ALLOW)
        l = ldap.initialize(ldap_server_url)
        l.protocol_version = ldap.VERSION2
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.simple_bind_s(ldap_server_login, ldap_server_password)
        return l
    except ldap.INVALID_CREDENTIALS, e:
        eprint(e)
        quit()
    except ldap.LDAPError, e:
        eprint(e)
        quit()


parser = OptionParser()

parser.add_option('-s', '--ldap_server', dest='ldap_server',
                  help='ldap server', metavar='LDAPSERVER')

parser.add_option('-u', '--ldap_login', dest='ldap_login',
                  help='ldap login', metavar='LDAPLOGIN')

parser.add_option('-b', '--ldap_bind', dest='ldap_bind',
                  help='ldap bind', metavar='LDAPBIND')

parser.add_option('-x', '--ldap_password', dest='ldap_password',
                  help='ldap password', metavar='LDAPPASSWORD')

parser.add_option(
    '-f',
    '--output_filename',
    dest='output_filename',
    help='output filename',
    metavar='OUTPUTFILENAME',
    default='result.csv',
    )

parser.add_option('-e', '--export_entry', dest='export_entry',
                  help='export entry', metavar='EXPORTENTRY')

parser.add_option(
    '-p',
    '--certif_filename',
    dest='certif_filename',
    help='certif filename',
    metavar='CERTIFFILE',
    default='',
    )

parser.add_option(
    '-k',
    '--entry_header',
    dest='entry_header',
    help='entry header',
    metavar='ENTRYHEADER',
    default='Entry PK',
    )

parser.add_option(
    '-l',
    '--lines_separator',
    dest='lines_separator',
    help='lines_separator',
    metavar='LINESEP',
    default='\n',
    )

parser.add_option(
    '-c',
    '--columns_separator',
    dest='columns_separator',
    help='columns_separator',
    metavar='COLSEP',
    default='|',
    )

parser.add_option(
    '-v',
    '--values_separator',
    dest='values_separator',
    help='vaues_separator',
    metavar='VALUESSEP',
    default='\n',
    )

(options, args) = parser.parse_args()

ldap_server_url = options.ldap_server
ldap_server_login = options.ldap_login
ldap_server_password = options.ldap_password
ldap_bind_url = options.ldap_bind

entry_to_export = options.export_entry
output_filename = options.output_filename
certif_filename = options.certif_filename
entry_header_name = options.entry_header

line_separator = options.lines_separator
columns_separator = options.columns_separator
value_elems_separator = options.values_separator

l = initLDAP(ldap_server_url, ldap_server_login, ldap_server_password,
             certif_filename)

LDAPEntries = getEntryFromDN(l, entry_to_export + ',' + ldap_bind_url)
saveElemsToCSVFile(LDAPEntries, entry_header_name, output_filename)

print('dump successful')
