# -*- coding: utf-8 -*-
import unittest
import logging

# from gstomd.corpus import GsuiteToMd
# from gstomd.settings import SetupLogging

logger = logging.getLogger(__name__)


class CorpusTest(unittest.TestCase):
    """Tests operations of corpus class.
    """

    # ga = GoogleAuth('settings/test1.yaml')
    # ga.LocalWebserverAuth()
    # drive = GoogleDrive(ga)

    def test_01(self):
        logger.debug("Begin")

        # gstomd = GsuiteToMd("settings/test1.yaml")
        # logger.debug("gsuiteTomd  Created")

        #     gstomd.Folder(
        #         folder_id="1Ue7U59r_oBXnuAtIOFkb8KGeTKAEZrkf",
        #
        #         root_folder_name="newposts",
        #     )
        # logger.debug("folders  Fetched")

        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
