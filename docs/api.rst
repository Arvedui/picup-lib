API documentation
=================

.. automodule:: picuplib

Picuplib basicly provides to different interfaces a function based and a class
based. The class based just wrapps the function based but stores the apikey and
default settings for the resize, rotation and noexif attribiutes.

.. autofunction:: upload

.. autofunction:: remote_upload


:class:`Upload`

.. autoclass:: Upload

.. automethod:: Upload.upload

.. automethod:: Upload.remote_upload


Allowed Values for the resize parameter are:

- 80x80
- 100x75
- 100x100
- 150x112
- 468x60
- 400x400
- 320x240
- 640x480
- 800x600
- 1024x768
- 1280x1024
- 1600x1200
- og

og is a german abbreviation for "original size"
