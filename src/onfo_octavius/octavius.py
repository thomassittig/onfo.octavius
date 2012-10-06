# -*- coding: utf-8 -*-

"""
the octavius module provides simply a way to store and relocate files
by this, it is producing a handler-object which represents one or many
versions of the same file

the specific handler class is responsible for creating and identifing
it multiple versions of it one master-file

the defined and used storage engine on the other hand is only responsible
for storing the physical information of a file into a unspecified storage
and providing a information-object with all the required data to remapping
the versions for an @AssetHandler


usage:

# define a file handler
class GalleryImage(AssetHandler):
    thumbnail = Image(filters=())


# create a default storage engine
engine = DefaultStorage(credentials)

# create a manager to handle this type
manager = AssetManager(GalleryImage, engine)

image_handler = manager.create(StreamIO, filename)

# every handler a the original, never touched, file itself as "master"-property
print image_handler.master
print image_handler.master.original_filename
print image_handler.master.path_to_file

# you can address a specific version by simple using the defined property
print image_handler.thumbnail
print image_handler.thumbnail.original_filename
print image_handler.thumbnail.path_to_file

# you can also iterate through the available versions. this do not include
# the master-reference
for image in image_handler:
    print image
    print image.original_filename
    print image.path_to_file




"""



import StringIO
import collections, logging, os, re
from os import path
import supersteiniwww.models as models
import supersteiniwww.lib.common as co
import transaction



log = logging.getLogger(__name__)

class AssetHandler(object):
    def __init__(self, storage_engine):
        pass

    def update(self, stream):
        # check ident-duplications in all versions
        # iterate through versions
        # execute filters
        # determine unique ident for each version
        # store resulting stream
        pass


class AssetManager(object):
    def __init__(self, handler_clazz, storage_engine):
        self.handler_clazz = handler_clazz
        self.storage_engine = storage_engine

    def create(self, stream):
        handler = self.handler_clazz(self.storage_engine)
        handler.update(stream)
        return handler

    def load(self, ident):
        stream = self.storage_engine.load(ident)
        return self.handler_clazz(stream, self.storage_engine)



