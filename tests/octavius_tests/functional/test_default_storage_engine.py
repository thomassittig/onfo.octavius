# -*- coding: utf-8 -*-

import unittest, StringIO
import onfo.octavius.engines.default as se

from octavius_tests import load_config

import sqlalchemy.orm as sqla_orm
from zope.sqlalchemy import ZopeTransactionExtension

def initialize_sql(engine, dbsession):
    dbsession.configure(bind=engine)
    se.Base.metadata.bind = engine
    se.Base.metadata.drop_all(engine)
    se.Base.metadata.create_all(engine)

class DefaultStorageEngineTest(unittest.TestCase):
    def setUp(self):
        from sqlalchemy import create_engine

        conf = load_config().get("functional", dict())
        self.dbsession = sqla_orm.scoped_session(sqla_orm.sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))

        dbengine = create_engine(conf.get(u"sqlite_conn_str"))
        initialize_sql(dbengine, self.dbsession)

        credentials = se.Credentials(conf.get("storage_dir"), self.dbsession)
        self.engine = se.DefaultStorageEngine(credentials)

    def tearDown(self):
        self.dbsession.remove()
        
    def test_create_engine(self):
        credentials = se.Credentials(None, None)
        engine = se.DefaultStorageEngine(credentials)
        
        self.assertFalse(engine is None)
        

    def test_store(self):
        """ storing a string as file and expect a FileInfo-objekt
        """
        stream = StringIO.StringIO("foo")

        file = self.engine.store(stream, u"foo.jpg", u"image/jpeg")

        self.assertFalse(file is None)

    def test_load(self):
        """ load a already stored file by using a Ident-object as identifier
        """
        stream = StringIO.StringIO("foo")
        stored = self.engine.store(stream, u"foo.jpg", u"image/jpeg")
        
        ident = se.Ident(1, None, None)
        file = self.engine.load(ident)

        self.assertFalse(file is None)
