# -*- coding:utf8 -*-
######################## BEGIN LICENSE BLOCK ########################
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
######################### END LICENSE BLOCK #########################

from __future__ import unicode_literals, print_function

from requests import post
from json import loads

from picuplib.exceptions import WrongResize, WrongRotation, UnsupportedFormat

API_URL = 'https://picflash.org/tool.php'

ALLOWED_SIZE = ('80x80', '100x75', '100x100', '150x112', '468x60', '400x400',
                '320x240', '640x480', '800x600', '1024x768', '1280x1024',
                '1600x1200', 'og')

ALLOWED_ROTATION = ('00', '90', '180', '270')

def upload_pic(api_key, pic, size='og', rotation='00', noexif=False):
    check_rotation(rotation)
    check_size(size)

    with open(pic, 'rb') as file_obj:
        post_data = {
                'Datei[]': file_obj,
                'formatliste': ('', size),
                'userdrehung': ('', rotation),
                'apikey': ('', api_key)
            }

        if noexif:
            post_data['noexif'] = ('', '')

        response = post(API_URL, files=post_data)

    check_reponse(response.text)
    return response.json()

def check_rotation(rotation):
    """checks rotation parameter if illegal value raises exception"""

    if rotation not in ALLOWED_ROTATION:
        allowed_rotation = ', '.join(ALLOWED_ROTATION)
        raise WrongRotation('Rotation %s is not allwoed. Allowed are %s'
                            % (rotation, allowed_rotation))

def check_size(size):
    """checks size parameter if illegal value raises exception"""

    if size not in ALLOWED_SIZE:
        allowed_size = ', '.join(ALLOWED_SIZE)
        raise WrongResize('Size %s is not allowed. Allowed are %s'
                          % (size, allowed_size))

def check_reponse(response):
    response = response.replace('null', '')
    if 'failure' in loads(response):
        raise UnsupportedFormat('Please look at picflash.org '
                                'witch formats are supported')
