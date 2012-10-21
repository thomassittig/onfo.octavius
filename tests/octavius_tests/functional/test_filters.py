# -*- coding: utf-8 -*-

import unittest, StringIO
import onfo.octavius.handler as ah
import onfo.octavius.engines.default as de

class AssetManagerTest(unittest.TestCase):
    def setUp(self):
        self.engine = None

    def tearDown(self):
        pass

    def test_default_instantiation(self):
        manager = ah.AssetManager()
        self.assertFalse(manager is None)

    def test_default_create(self):
        manager = ah.AssetManager()
        file_handler = manager.create(StringIO.StringIO("foo"))
        self.assertFalse(file_handler is None)
    
    def test_default_load(self):
        manager = ah.AssetManager()
        file_handler = manager.load(de.Ident(1, None, None))
        self.assertFalse(file_handler is None)

