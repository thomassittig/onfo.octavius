# -*- coding: utf-8 -*-

#
# simple concept
#

if False:
    class GalleryImage(AssetHandler):
        thumbnail = Image(filters=(Resize(120,120),))
        large = Image(filters=(Resize(1024,768),Watermark(StreamIO)))


    class PrintDropbox(AssetHandler):
        _allowed_ = (Zip(), Images(),)

    class PdfFile(AssetHandler):
        _allowed_ = (PDF(), )

    # image asset
    engine = StorageEngine(credentials, user_id)
    manager = AssetManager(GalleryImage, engine)


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
    engine = StorageEngine(credentials, user_id)
    manager = AssetManager.create(GalleryImage, engine)

    file_handler = manager.create(stream, filename, mime_type)
    print file_handler.ident()
    print file_handler.master.original_filename


    # upload print asset of image or zip type
    engine = StorageEngine(credentials, user_id)
    manager = AssetManager.create(PrintDropbox, engine)

    handler = manager.create_new(stream, filename)

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


if True:

    class Meta(object):
        pass

    class Base(object):
        # __metaclass__ = Meta

        foo = Meta()

        pass

    o = Base()

    print o.foo
    print Base.foo
    print o.foo == Base.foo

    o.foo = 1

    print o.foo
    print Base.foo
    print o.foo == Base.foo




