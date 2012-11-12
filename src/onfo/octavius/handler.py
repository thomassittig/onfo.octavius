# -*- coding: utf-8 -*-
""" the octavius module provides simply a way to store and relocate files
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
>>> class GalleryImage(AssetHandler):
>>>     thumbnail = Image(filters=())


# create a default storage engine
>>> engine = DefaultStorage(credentials)

# create a manager to handle this type
>>> manager = AssetManager(GalleryImage, engine)

>>> image_handler = manager.create(StreamIO, filename)

# every handler a the original, never touched, file itself as "master"-property
>>> print image_handler.master
FileInfo()

>>> print image_handler.master.file.original_filename
some_filename.jpg

>>> print image_handler.master.file.path_to_file
/path/to/physical/file

# you can address a specific version by simple using the defined property
>>> print image_handler.thumbnail
FileInfo()

>>> print image_handler.thumbnail.file.original_filename
some_filename.jpg

>>> print image_handler.thumbnail.file.path_to_file
/path/to/physical/file

# you can also iterate through the available versions. this do not include
# the master-reference
>>> for image in image_handler:
>>>     print image
>>>     print image.original_filename
>>>     print image.path_to_file

# an AssetHandler has also it's own ident
>>> print image_handler.ident()
"""



import StringIO
import collections, logging, os, re

import filters as filt

log = logging.getLogger(__name__)

def extension():

    table = {
        'text/plain': '.txt',
        'text/html': '.html',
        'text/xml': '.xml',
        'text/css': '.css',
        'text/csv': '.csv',
        'application/postscript': '.ps',
        'application/vnd.ms-excel': '.xsl',
        'application/xml': '.xml',
        'application/msword': '.doc',
        'application/pdf': '.pdf',
        'image/png': '.png',
        'image/jpeg': '.jpg',
        'image/gif': '.gif',
        'image/tiff': '.tif',
        }

    def resolve(type):
        return table.get(type, ".data")

    return resolve


extension = extension()

class FileAccessHandler:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        
    def __enter__(self):
        try:
            self.pointer = open(self.path_to_file, "rw")
            log.debug(u"opened a existing file (file=%s)", self.path_to_file)
        except IOError as e:
            self.pointer = open(self.path_to_file, "w+b")
            log.debug(u"create a new file (file=%s)", self.path_to_file)
            
        return self.pointer
    
    def __exit__(self, type, value, traceback):
        self.pointer.close()

class FileInfo(object):

    ident = None
    original_filename = None
    mime_type = None
    path_to_file = None
    full_path_to_file = None
    
    def file_handler(self):
        """ returns a access handler to the current file in the filesystem
        """
        dirname = os.path.dirname(self.full_path_to_file)
        
        if not os.path.isdir(dirname):
            log.debug(u"create new directory for %s" % dirname)
            os.makedirs(dirname)

        return FileAccessHandler(self.full_path_to_file)
    
    def __repr__(self):
        return u"<FileInfo(ident=%s, original_filename=%s, mime_type=%s, path_to_file=%s, full_path_to_file=%s)>" % (self.ident, 
                                                                                                                     self.original_filename, 
                                                                                                                     self.mime_type, 
                                                                                                                     self.path_to_file, 
                                                                                                                     self.full_path_to_file)

class FileVersion(object):
    """ FileVersion´s are templates which define how byte-data should be with proceeded
    The real byte/file-informations are accessable through the file()-method
    """
    _allowed_ = None
    
#    def __call__(self, file_info):
#        """ initializing a file-version with the matching FileInfo 
#        """
#        self._file_info = file_info
        
    
    def update(self, engine, source_info):
        """ creating a copy of the file-data, specified in source_info and create a new version of it
        
        engine : StorageEngine
        source_info : onfo.octavius.handler.FileInfo 
        """
        file_content = None
        
        with source_info.file_handler() as iostream:
            file_content = iostream.read()
            
        self.file = engine.store(file_content, source_info.original_filename, source_info.mime_type)
    
    def __get__(self, instance, clazz):
        indexer = self.__resolve_indexer(instance)
        
        if not indexer in instance.__dict__.keys():
            instance.__dict__[indexer] = None
        
        return instance.__dict__[indexer]
            
    def __set__(self, instance, value):
        
        if not isinstance(value, FileInfo):
            raise ValueError(u"jus object of type FileInfo are allowed")
        
        indexer = self.__resolve_indexer(instance)
        instance.__dict__[indexer] = value
        
    
    def __resolve_indexer(self, instance):
        
        print "_resolve: ", dir(instance)
        
        for k,v in instance.__dict__.iteritems():
            print "v: ", v, self
            if v is self: return self.indexer(k)
        
        raise Exception(u"THIS object is not a part of the given instance")
        

    def __indexer(self, name):
        return u"__{%s}" % name
    
    @property
    def file(self):
        """ returns the real physical representation of the current file-version
        """
        return self._file_info



class Image(FileVersion):
    """ Image is a superset of FileVersion, which contains a unmutable range of accepted filetypes
    """
    def __init__(self, filters=None):
        super(Image, self).__init__()
        self._allowed_ = (filt.Jpeg(), filt.Gif(), filt.Png(),)

class AssetHandler(object):
    
    master = FileVersion()
    
    __bindings = None
    
    def __init__(self, master, storage_engine):
        self.master(storage_engine, master)
        self._se = storage_engine
        self.__bindings = dict()
        
        # init versions
        for k,v in self.__dict__.iteritems():
            element = self.__dict__.get(k)
            if isinstance(element, FileVersion):
                self.__bindings[k] = element
            
        
    def __getattr__(self, name):
        if name in self.__bindings.keys():
            return self.__bindings.get(name)
        
        return self.__dict__.get(name)
        
    @property
    def display_name(self):
        raise Exception("not implemented yet")
        
    @property
    def ident(self):
        """ the primary ident for a AssetHandler
        
        it is regardless, if the ident of the master or any
        subversion will be used, because the original master
        will be determined based on the ident-properties.
        but for simplifications we should address the
        master-asset
        """
        return self.master.file.ident

    def update(self):
        """ create or update all physical file-versions of the the master-asset
        """
        # check ident-duplications in all versions
        # iterate through versions
        # execute filters
        # determine unique ident for each version
        # store resulting stream
        for k,file_version in self.__bindings.iteritems():
            file_version.update(self._se, self.master.file)



class AssetManager(object):
    def __init__(self, handler_clazz, storage_engine):
        self.handler_clazz = handler_clazz
        self.storage_engine = storage_engine

    def create(self, file_content, filename, mime_type=None):
        file_info = self.storage_engine.store(file_content, filename, mime_type)
        handler = self.handler_clazz(file_info, self.storage_engine)
        handler.update()
        return handler

    def load(self, ident):
        master_asset = self.storage_engine.load(ident)
        return self.handler_clazz(master_asset, self.storage_engine)


if __name__ == "__main__":
    
    class Value(object):
        
        def key(self, klazz):
            for k,v in klazz.__dict__.iteritems():
                if v is self: return "__%s_%s" % (self.__class__, k)
            
            raise Exception(u"a instance of this class could not be found")
            
        
        def __set__(self, instance, value):
            instance.__dict__[self.key(instance.__class__)] = value
        
        def __get__(self, instance, owner):
            return instance.__dict__.get(self.key(owner))
        
        def update(self, value):
            self = value
    
    class MetaValueHandler(type):
        def __new__(mcs, name, bases, dict):
            print "mcs, name, bases, dict: ", mcs, name, bases, dict
        
    
    class ValueHandler(object):
        __metaclass__ = MetaValueHandler
    
    class Collection(object):
        foo = ValueHandler()
        bar = ValueHandler()
            

    o1 = Collection(1,2)
    o2 = Collection()
    
    
    print "start"
    
    o = ValueHandler()
        
        