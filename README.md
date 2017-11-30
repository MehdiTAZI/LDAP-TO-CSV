# LDAP-TO-CSV
LDAP to CSV Pyhton script

this script dump LDAP entries (ou=) to a CSV file with a const number of columns according to the following mapping :
- the columns will be constant between all the csv lines
- each columns will have as key the entry id
- the header will be the name of the attributs and the uid attribut header name can be choosen
- if many values exists within the same column, they will be separated using a configurable separator ( by default # )
- it works with unsecure and secure LDAP( using certificates )
- du to it CSV mapping in with a const columns number, it can be easly converted to RDBMS schema

