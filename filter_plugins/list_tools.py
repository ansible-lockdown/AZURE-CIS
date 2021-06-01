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

class FilterModule(object):
    ''' Ansible filters for lists '''

    def filters(self):
        return { 'get_list_item': self.get_list_item }

    def get_list_item(self, list, key, value):
        return next(item for item in list if item[key] == value)

