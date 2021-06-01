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

AZ_BASE_URL = 'https://management.azure.com'
AZ_API_VERSIONS = [ 
    "2017-10-01-preview",
    "2017-05-01",
]
AZ_PROVIDERS = [
    "Microsoft.Authorization"
]

class FilterModule(object):
    ''' Ansible filters for Azure Management API '''

    def az_version(self, api_version):
        if api_version in AZ_API_VERSIONS:
            return api_version
        else:
            raise AnsibleFilterError(
                'Invalid API Version: [{api_version}]. MS Graph Version must be one of [{api_version_list}].'.format(
                    api_version = api_version, 
                    api_version_list = ', '.join(AZ_API_VERSIONS)
                ), 
                show_content=True
            )

    def az_base_url(self, subscription):
        return "{base_url}/subscriptions/{subscription}".format(
            base_url = AZ_BASE_URL, 
            subscription = subscription
        )

    def az_provider_url(self, subscription, provider):
        return "{base_url}/providers/{provider}".format(
            base_url = self.az_base_url(subscription), 
            provider = provider
        )

    def az_list_role_definitions(self, subscription, api_version = '2017-05-01'):
        return "{base_url}/roleDefinitions?api-version={api_version}".format(
            base_url = self.az_provider_url(subscription, "Microsoft.Authorization"), 
            api_version = api_version
        )

    def az_list_role_assignments(self, subscription, api_version = '2017-10-01-preview'):
        return "{base_url}/roleAssignments?api-version={api_version}".format(
            base_url = self.az_provider_url(subscription, "Microsoft.Authorization"), 
            api_version = api_version
        )

    def filters(self):
        return {
            'az_version': self.az_version,
            'az_base_url': self.az_base_url,
            'az_provider_url': self.az_provider_url,
            'az_list_role_definitions': self.az_list_role_definitions,
            'az_list_role_assignments': self.az_list_role_assignments,
        }

