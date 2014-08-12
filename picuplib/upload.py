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
"""
This module handels the entire upload and some argument and response checking
"""

from __future__ import unicode_literals, print_function

from requests import post

from picuplib.checks import (check_size, check_rotation, check_noexif,
                             check_response)

from picuplib.globals import API_URL

class Upload(object):
    """
    Class based wrapper for uploading.
    It stores the apikey and default settings for size, rotation …
    """

    def __init__(self, apikey, size='og', rotation='00', noexif=False):
        self._apikey = apikey
        self._size = size
        self._rotation = rotation
        self._noexif = noexif

    @property
    def size(self):
        """getter for _size"""
        return self._size

    @size.setter
    def size(self, value):
        """setter for _size"""
        check_size(value)
        self._size = value

    @property
    def rotation(self):
        """getter for _rotation"""
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        """setter for rotation"""
        check_rotation(value)
        self._rotation = value

    @property
    def noexif(self):
        """getter for _noexif"""
        return self._noexif

    @noexif.setter
    def noexif(self, value):
        """setter for _noexif"""
        check_noexif(value)
        self._noexif = value

    def upload(self, picture, size=None, rotation=None, noexif=None):
        """wraps upload function"""
        if not size:
            size = self._size
        if not rotation:
            rotation = self._rotation
        if not noexif:
            noexif = self._noexif

        return upload(self._apikey, picture, size, rotation, noexif)

    def remote_upload(self, picture_url, size=None, rotation=None, noexif=None):
        """wraps remote_upload funktion"""
        if not size:
            size = self._size
        if not rotation:
            rotation = self._rotation
        if not noexif:
            noexif = self._noexif

        return remote_upload(self._apikey, picture_url, size, rotation, noexif)


def upload(apikey, picture, size='og', rotation='00', noexif=False):
    """
    prepares post for regular upload
    """
    check_rotation(rotation)
    check_size(size)

    post_data = compose_post(apikey, size, rotation, noexif)

    with open(picture, 'rb') as file_obj:
        post_data['Datei[]'] = file_obj

        return do_upload(post_data)

def remote_upload(apikey, picture_url, size='og', rotation='00', noexif=False):
    """
    prepares post for remote upload
    """
    check_rotation(rotation)
    check_size(size)

    post_data = compose_post(apikey, size, rotation, noexif)
    post_data['url[]'] = ('', picture_url)

    return do_upload(post_data)



def compose_post(apikey, size, rotation, noexif):
    """
    composes basic post requests
    """
    check_rotation(rotation)
    check_size(size)

    post_data = {
        'formatliste': ('', size),
        'userdrehung': ('', rotation),
        'apikey': ('', apikey)
        }

    if noexif:
        post_data['noexif'] = ('', '')

    return post_data

def do_upload(post_data):
    """
    does the actual upload
    """
    response = post(API_URL, files=post_data)
    check_response(response.text)

    return response.json()

