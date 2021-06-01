# Copyright 2021, Rick Culpepper <rick@refactr.it>
#
# list_tools.py is a custom filter for Ansible
#
# azure_tools.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# azure_tools.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError, AnsibleFilterTypeError

import types, json

MSGRAPH_BASE_URL = 'https://graph.microsoft.com'
MSGRAPH_DEFAULT_SCOPE = '.default'
MSGRAPH_DEFAULT_VERSION = 'v1.0'
MSGRAPH_VERSIONS = [ 'beta', MSGRAPH_DEFAULT_VERSION ]
MSGRAPH_STRONG_AUTHENTICATION_METHODS = [ 
    'fido2Methods', 
    'microsoftAuthenticationMethods', 
    'windowsHelloForBusinessMethods', 
    'temporaryAccessPassMethods', 
    'phoneMethods', 
    'emailMethods' 
]

class FilterModule(object):
    ''' Ansible filters for Microsft Graph API '''

    def msgraph_scope(self, scopes):
        if scopes is None:
            scopes = MSGRAPH_DEFAULT_SCOPE
        if isinstance(scopes,list):
            scopes = ','.join(scopes)
        return "{base_url}/{scopes}".format(
            base_url=MSGRAPH_BASE_URL, 
            scopes=scopes
        )
    
    def msgraph_version(self, version):
        if version is None or len(version) == 0:
            return MSGRAPH_DEFAULT_VERSION
        elif version in MSGRAPH_VERSIONS:
            return version
        else:
            raise AnsibleFilterError(
                'Invalid Version: [{version}]. MS Graph Version must be one of [{version_list}].'.format(
                    version = version, 
                    version_list = ', '.join(MSGRAPH_VERSIONS)
                ), 
                show_content=True
            )

    def msgraph_base_url(self, version=MSGRAPH_DEFAULT_VERSION):
        return "{base_url}/{version}".format(
            base_url = MSGRAPH_BASE_URL, 
            version = self.msgraph_version(version)
        )

    def msgraph_list_users(self, querystring, version=MSGRAPH_DEFAULT_VERSION):
        return "{base_url}/users{qs}".format(
            base_url = self.msgraph_base_url(version), 
            qs = '?'+querystring if querystring else ''
        )

    def msgraph_user_strong_authentication_method(self, id, method, version="beta"):
        if method not in MSGRAPH_STRONG_AUTHENTICATION_METHODS:
            raise AnsibleFilterError(
                'Invalid method: [{method}]. Strong Authentication Method must be one of [{method_list}].'.format(
                    method = method,
                    method_list = ', '.join(MSGRAPH_STRONG_AUTHENTICATION_METHODS)
                ),
                show_content=True
            )
        return "{msgraph_list_users}/{pid}/authentication/{method}".format(
            msgraph_list_users=self.msgraph_list_users(version),
            pid=id,
            method=method
        )

    def msgraph_user_strong_authentication_methods(self, id, version="beta"):
        urls = []
        for method in MSGRAPH_STRONG_AUTHENTICATION_METHODS:
            urls.append(
                self.msgraph_user_strong_authentication_method(id, method, version=version)
            )       
        return urls
    
    def filters(self):
        return {
            'msgraph_scope': self.msgraph_scope,
            'msgraph_version': self.msgraph_version,
            'msgraph_base_url': self.msgraph_base_url,
            'msgraph_list_users': self.msgraph_list_users,
            'msgraph_user_strong_authentication_method': self.msgraph_user_strong_authentication_method,
            'msgraph_user_strong_authentication_methods': self.msgraph_user_strong_authentication_methods
        }

