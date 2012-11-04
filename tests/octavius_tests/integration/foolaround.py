# -*- coding: utf-8 -*-
""" this module contains a simple example about how 
the octavius-api could be used to
"""
import StringIO, unittest

from onfo.octavius.handler import AssetManager, AssetHandler, Image
import onfo.octavius.filters as filters
import onfo.octavius.engines.default as se

DefaultStorageEngine = se.DefaultStorageEngine
Credentials = se.Credentials

from octavius_tests import load_config


Resize = filters.Resize
Watermark = filters.Watermark
Resize = filters.Resize

#
# simple concept
#
class GalleryImage(AssetHandler):
    thumbnail = Image(filters=(Resize(120,120),))
    large = Image(filters=(Resize(1024,768),Watermark(StringIO)))


class PrintDropbox(AssetHandler):
    _allowed_ = (filters.Zip(), filters.Images(),)

class PdfFile(AssetHandler):
    _allowed_ = (filters.Pdf(), )

def initialize_sql(engine, dbsession):
    dbsession.configure(bind=engine)
    se.Base.metadata.bind = engine
    se.Base.metadata.drop_all(engine)
    se.Base.metadata.create_all(engine)


def _store_jpeg(config, manager):
    file_path = config.get("jpeg_image")
    file_content = None
    
    with open(file_path) as stream:
        file_content = stream.read()
    
    return manager.create(file_content, "foo.jpg", mime_type="image/jpeg")

class AbstractImageTest(unittest.TestCase):
    """ providing / initializing a default database for integration tests
    """
    def setUp(self):
        super(AbstractImageTest, self).setUp()
        from sqlalchemy import create_engine
        import sqlalchemy.orm as sqla_orm
        from zope.sqlalchemy import ZopeTransactionExtension
        
        unittest.TestCase.setUp(self)
        
        self.conf = load_config().get("integration", dict())
        
        self.dbsession = sqla_orm.scoped_session(sqla_orm.sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))

        dbengine = create_engine(self.conf.get(u"sqlite_conn_str"))
        initialize_sql(dbengine, self.dbsession)

    def tearDown(self):
        self.dbsession.remove()
    

class TestImageExample(AbstractImageTest):
    """ store and load an image file
    """
    #user_id = 1
    #credentials = None
    #stream = StringIO.StringIO("unspecific file content")
    #filename = "file.png"
    #mime_type = "image/png"

    def setUp(self):
        super(TestImageExample, self).setUp()
        
        credentials = se.Credentials(self.conf.get("storage_dir"), self.dbsession)
        self.engine = se.DefaultStorageEngine(credentials)
        self.manager = AssetManager(GalleryImage, self.engine)

    def test_create(self):
        stored_image = _store_jpeg(self.conf, self.manager)
        self.assertFalse(stored_image is None)
        
        self.assertFalse(stored_image.ident is None)
        self.assertFalse(stored_image.display_name is None)
        
        file = stored_image.master.file
        
        self.assertFalse(file.original_filename is None)
        self.assertFalse(file.path_to_file is None)
        self.assertFalse(file.relative_path_to_file is None)

        file = stored_image.thumbnail
        
        self.assertFalse(file.original_filename is None)
        self.assertFalse(file.path_to_file is None)
        self.assertFalse(file.relative_path_to_file is None)

        file = stored_image.large
        
        self.assertFalse(file.original_filename is None)
        self.assertFalse(file.path_to_file is None)
        self.assertFalse(file.relative_path_to_file is None)
        
        
    
    def test_load(self):
        foo = _store_jpeg(self.conf, self.manager)
        
        stored_image = self.manager.load(foo.ident)
        
        self.assertFalse(stored_image is None)



class TestPdfExample(unittest.TestCase):
    """ store and load an pdf-file
    the difference to the image-file example is, that this filetype has no
    special versions to consider
    """


if False:
    # image asset
    
    image_handler = GalleryImage(stream, filename, mime_type)
    image_handler = manager.create(stream, filename, mime_type)
    
    #builder  = GalleryImage()
    #builder.thumbnail.filters.add(Watermark(StreamIO))
    
    #engine = StorageEngine(credentials, user_id)
    #manager = AssetManager.create(builder, engine)
    #handler = manager.create(StreamIO, display_name)
    
    print image_handler.ident()
    print image_handler.display_name
    
    # the original, never touched file
    print image_handler.master.original_filename
    print image_handler.master.path_to_file
    
    thumbnail = image_handler.thumbnail
    print thumbnail.original_filename
    print thumbnail.path_to_file
    print thumbnail.relative_path_to_file
    
    handler = manager.load(image_handler.ident())
    
    # simple file management
    engine = DefaultStorageEngine(credentials, user_id)
    manager = AssetManager.create(GalleryImage, engine)
    
    file_handler = manager.create(stream, filename, mime_type)
    print file_handler.ident()
    print file_handler.master.original_filename
    
    
    # upload print asset of image or zip type
    engine = DefaultStorageEngine(credentials, user_id)
    manager = AssetManager.create(PrintDropbox, engine)
    
    handler = manager.create_new(stream, filename)

if False:
    # an experimantal sample for implementing / using produced assets
    # in an sortable collection-structure
    # handle collections
    manager = CollectionManager()
    collection = manager.create(display_name)
    collection.add(handler,0, "description")
    collection.add(handler,1)
    collection.add(handler,2, "description")
    collection.add((handler,handler,handler,))
    
    field1 = collection.add_field(label, description, index)
    field2 = collection.add_field(label, description, index)
    
    collection.update_fields((field1,field2,))
    collection.update_fields((field2,field1,)) #reverse ordering
    
    fields = collection.fields
    print fields.totalCount
    print fields.entries




