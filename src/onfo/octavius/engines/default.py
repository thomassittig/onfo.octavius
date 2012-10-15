# -*- coding: utf-8 -*-

# This module is part of onfo_octavius and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
#
# this enine is used by the onfo_ocatvius asset management module
# it describes, how a filestream will be saved to the filesystem
# and registered/referenced in a database
#

import logging, collections, sqlalchemy, datetime, transaction

import sqlalchemy.ext.declarative as sqla_decl

#import declarative_base

import sqlalchemy.orm as sqla_orm

#from sqlalchemy.orm import (
#    scoped_session,
#    sessionmaker,
#    relationship,
#    )

from zope.sqlalchemy import ZopeTransactionExtension

#DBSession = sqla_orm.scoped_session(sqla_orm.sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
Base = sqla_decl.declarative_base()


log = logging.getLogger(__name__)

# The Ident-object provides the required information for determining 
# a unique, file-specific naming
Ident = collections.namedtuple("Ident", ("id", "parent_id", "str1",))
Credentials = collections.namedtuple("Credentials", ("storage_directory", "alchemy_session",))

def determine_filepath(int_key, str_key):
    pass


class FileInfo(object):

    ident = Ident(None, None, None)
    original_filename = None
    mime_type = None
    path_to_file = None
    full_path_to_file = None

    def __init__(self, data):
        self._data = data

        self.ident = Ident(data.id, data.parent_id, data.str1)
        self.original_filename = data.original_filename
        self.mime_type = data.mime_type

        self.path_to_file = determine_filepath(data.id, data.mime_type)


class Asset(Base):
    __tablename__ = 'asset'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    original_filename = sqlalchemy.Column(sqlalchemy.VARCHAR(255), nullable=False)
    mime_type = sqlalchemy.Column(sqlalchemy.VARCHAR(10), nullable=False)
    str1 = sqlalchemy.Column(sqlalchemy.VARCHAR(100), nullable=True)
    created_on = sqlalchemy.Column(sqlalchemy.DATETIME, nullable=False, default=datetime.datetime.utcnow)
    modified_on = sqlalchemy.Column(sqlalchemy.DATETIME, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, original_filename, mime_type):
        self.original_filename = original_filename
        self.mime_type = mime_type

    def __repr__(self):
        return u"Asset(id=%s, parent_id=%s, str1=%s, mime_type=%s, )" % (self.id, self.parent_id, self.str1, self.mime_type)


class DefaultStorageEngine(object):
    def __init__(self, credentials):
        self.storage_directory = credentials.storage_directory
        self.alchemy_session = credentials.alchemy_session

    def store(self, stream, filename, mime_type, ident=Ident(None, None, None)):
        log.info(u"register a asset to the database (filename=%s, mime_type=%s, ident=%s)" % (filename, mime_type, ident))
        data = Asset(filename, mime_type)

        with transaction.manager:
            self.alchemy_session.add(data)

        #filepath = determine_filepath(data.id, mime_type)

        return FileInfo(data)

    def load(self, ident):
        data = None
        
        if ident.id is None:
            raise ValueError(u"ID-value can not be None (data=%s)"  % ident.id)
        
        with transaction.manager:
            query = self.alchemy_session.query(Asset)
            query = query.filter(Asset.id==ident.id)
            
            if query.count() == 1:
                return FileInfo(query.first())
            
            log.info(u"no matching record could be found for the given ident (ident=%s)" % ident)
        
        return None
