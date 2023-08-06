# -*- coding: utf-8 -*-
import logging
import os
import re
import unicodedata
import zipfile
from datetime import datetime

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

logger = logging.getLogger(__name__)
FILETYPE = {
    "DOC": ("application/vnd.google-apps.document", "Google Doc"),
    "FOLDER": ("application/vnd.google-apps.folder", "Folder"),
}


DEFAULT_SETTINGS = {
    "pydrive_settings": "pydrive_settings.yaml",
    "dest_folder": "gstomd_extract",
}


def mime_to_filetype(mime_string):
    """convert mimi type in simple string

    Args:
        mime_string (string)

    Returns:
        string : [description]
    """
    for label, carac in FILETYPE.items():
        if carac[0] == mime_string:
            return label
    logger.debug("Unknown mime type : %s", mime_string)
    return "UNKNOWN"


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "", value).strip("-_")


class Node:
    """
    class for Google Drive item
    """

    def __init__(self, googleDriveFile, path="", depth=1, drive_connector=""):

        self._googleDriveFile = googleDriveFile
        self.drive_connector = drive_connector
        self.path = path
        self.depth = depth
        self.is_fetched = False

    def unix_name(self):
        return slugify(self.basename())

    def parent(self):
        if self.parents:
            return self.parents[0]["id"]
        return self.parents

    @property
    def parents(self):  # pass accesses to googleDriveFile
        if self._googleDriveFile:
            if self._googleDriveFile["parents"]:
                return self._googleDriveFile["parents"]

        return ""

    def id(self):  # pass accesses to googleDriveFile
        if self._googleDriveFile:
            return self._googleDriveFile["id"]
        return ""

    def basename(self):  # pass accesses to googleDriveFile
        if self._googleDriveFile:
            return self._googleDriveFile["title"]
        return ""


class Gdoc(Node):
    def __str__(self):
        return "\n%sD : %20s|%30s|%20s|%s" % (
            "-" * self.depth * 4,
            self.basename(),
            self.id(),
            self.unix_name(),
            self.path,
        )

    def fetch(self):
        logger.debug("fetch content for %s", self)
        self._googleDriveFile.FetchContent(
            mimetype="application/zip", remove_bom=True
        )
        self.is_fetched = True

    def to_disk(self):
        if not self.is_fetched:
            self.fetch()
        os.makedirs(self.path)
        zip_path = self.path + "/" + os.path.basename(self.path) + ".zip"
        md_path = self.path + "/" + os.path.basename(self.path) + ".md"
        f_zip = open(zip_path, "wb")
        f_zip.write(self._googleDriveFile.content.getvalue())
        f_zip.close()
        with zipfile.ZipFile(zip_path, "r") as zip_ref:

            files_names = zip_ref.namelist()
            for file_name in files_names:
                if file_name.endswith(".html"):
                    f_md = open(md_path, "w")
                    html = zip_ref.read(file_name)
                    parsed_html = BeautifulSoup(html, features="lxml")
                    body = "%s" % (parsed_html.body)

                    body_md = md(body)
                    f_md.write(body_md)
                    f_md.close()
                else:
                    zip_ref.extract(file_name, os.path.dirname(md_path))
            os.remove(zip_path)


class Gfolder(Node):
    def __init__(
        self,
        googleDriveFile="",
        path="",
        depth=1,
        drive_connector="",
        dest_folder="",
        root_folder_id="",
        root_folder_name="",
    ):
        super().__init__(
            googleDriveFile=googleDriveFile,
            path=path,
            depth=depth,
            drive_connector=drive_connector,
        )
        self.children = []
        self.dest_folder = dest_folder
        self.root_folder_name = root_folder_name
        self.root_folder_id = root_folder_id
        logger.debug(self)

    def __str__(self):
        message = "\n%sF : %20s|%30s|%20s|%s" % (
            "-" * self.depth * 4,
            self.basename(),
            self.id(),
            self.unix_name(),
            self.path,
        )
        for child in self.children:
            message = "%s%s" % (message, child)
        return message

    def fetch(self):
        """
        Generate folder structure with files
        """

        now = datetime.now()
        date_time = now.strftime("%Y.%m.%d.%H.%M.%S")
        self.path = "%s/%s/%s" % (
            self.dest_folder,
            self.root_folder_name,
            date_time,
        )
        logger.debug(".")
        nodes = {}
        query = (
            "trashed=false and mimeType='application/vnd.google-apps.folder'"
        )
        # file_list = pydrive_list_item(self.drive_connector, query)
        file_list = self.drive_connector.ListFile({"q": query}).GetList()

        file_list = self.drive_connector.ListFile(
            {
                "q": query,
                "corpora": "allDrives",
                "includeItemsFromAllDrives": True,
                "supportsAllDrives": True,
            },
        ).GetList()
        logger.debug("%d folders found", sum(1 for x in file_list))

        for item in file_list:
            if item["id"] == self.root_folder_id:
                self._googleDriveFile = item
                folder = self
                if not self.root_folder_name:
                    self.root_folder_id = folder.basename()
            else:
                folder = Gfolder(item)
            nodes[folder.id()] = (folder, folder.parent())

        for folder_id, (folder, parent_id) in nodes.items():

            if parent_id is None:
                continue
            if parent_id in nodes.keys():
                nodes[parent_id][0].children.append(folder)
            else:
                logger.debug("parent id %s not found ", parent_id)

        self.complement_children_path_depth()
        folders = self.all_subfolders()
        parents_id = " or ".join(
            "'{!s}' in parents".format(key) for key in folders
        )
        # parents_id = "%s or '%s' in parents" % (parents_id, folders)

        query_for_files = (
            "trashed=false and mimeType='application/vnd.google-apps.document' and ("
            + parents_id
            + ")"
        )

        logger.debug("Query for files : %s", query_for_files)
        file_list = self.drive_connector.ListFile(
            {
                "q": query_for_files,
                "corpora": "allDrives",
                "includeItemsFromAllDrives": True,
                "supportsAllDrives": True,
            },
        ).GetList()
        # file_list = pydrive_list_item(self.drive_connector, query_for_files)
        logger.debug("%d files found", sum(1 for x in file_list))

        for item in file_list:
            if mime_to_filetype(item["mimeType"]) != "DOC":
                logger.debug("%s %s", item["title"], item["mimeType"])
                continue
            doc = Gdoc(item)
            logger.debug("Doc found %s", doc)

            if doc.parent() in nodes.keys():
                nodes[doc.parent()][0].children.append(doc)
                logger.debug(
                    "doc added as children of %s", nodes[doc.parent()][0]
                )
            else:
                logger.debug("parent id %s not found", doc.parent())
        self.complement_children_path_depth()

        logger.debug(self)
        self.fetched = True
        return self

    def to_disk(self):
        os.makedirs(self.path)
        if self.children:
            for child in self.children:
                if isinstance(child, Gfolder):
                    child.to_disk()

                elif isinstance(child, Gdoc):
                    child.to_disk()

    def all_subfolders(self):
        """
        list all subfolders
        """
        list_folders = set()

        for child in self.children:
            if isinstance(child, Gfolder):
                list_folders.add(child.id())
                child_folders = child.all_subfolders()
                if child_folders:
                    list_folders = list_folders.union(child_folders)
        return list_folders

    def complement_children_path_depth(self):
        """
        generate children's path and depth information from basename
        """
        for child in self.children:
            child.path = "{0}/{1}".format(self.path, child.unix_name())
            child.depth = self.depth + 1
            if isinstance(child, Gfolder):
                child.complement_children_path_depth()


class GsuiteToMd:
    def __init__(
        self,
        pydrive_settings=DEFAULT_SETTINGS["pydrive_settings"],
        dest_folder=DEFAULT_SETTINGS["dest_folder"],
    ):
        """Create an instance of GsuiteToMd.

        """

        self.dest_folder = dest_folder
        self.pydrive_settings = pydrive_settings
        logger.info(
            "Settings : dest_folder %s, pydrive_settings %s",
            self.dest_folder,
            self.pydrive_settings,
        )
        self.ga = GoogleAuth(self.pydrive_settings)
        self.drive_connector = GoogleDrive(self.ga)

    def Folder(self, folder_id, root_folder_name=""):
        f = Gfolder(
            googleDriveFile="",
            path="",
            depth=1,
            drive_connector=self.drive_connector,
            root_folder_id=folder_id,
            dest_folder=self.dest_folder,
            root_folder_name=root_folder_name,
        )

        f.fetch()
        f.to_disk()

    def Gdoc(self, doc_id, dest_folder):
        doc = Gdoc(self.drive_connector, doc_id, dest_folder)
        doc.fetch()
        doc.to_disk()


class PyDriveRetriableError(Exception):
    pass
