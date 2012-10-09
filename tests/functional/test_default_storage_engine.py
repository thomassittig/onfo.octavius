# -*- coding: utf-8 -*-

import unittest, StringIO
import onfo_octavius.engines.default as se

from tests.functional import load_config

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

        conf = load_config().get("main", dict())
        self.dbsession = sqla_orm.scoped_session(sqla_orm.sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
        credentials = se.Credentials(conf.get("storage_directory"), self.dbsession)

        self.engine = se.DefaultStorageEngine(credentials)

        dbengine = create_engine(conf.get(u"sqlite_conn_str"))
        initialize_sql(dbengine, self.dbsession)


    def tearDown(self):
        self.dbsession.remove()


    def test_store(self):
        stream = StringIO.StringIO("foo")

        file = self.engine.store(stream, "foo.jpg")

        self.assertFalse(file is None)

    def test_load(self):
        ident = se.Ident(1, None, None)
        file = self.engine.load(ident)

        self.assertFalse(file is None)
