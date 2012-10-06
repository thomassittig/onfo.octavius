# -*- coding: utf-8 -*-

# This module is part of onfo_octavius and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#
# this enine is used by the onfo_ocatvius asset management module
# it describes, how a filestream will be saved to the filesystem
# and registered/referenced in a database
#

import logging

log = logging.getLogger(__name__)

class DefaultStorageEngine(object):
    def store(self, stream, filename):
        pass

    def load(self, ident):
        pass