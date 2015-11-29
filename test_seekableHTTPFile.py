import io
from unittest import TestCase
from zipfile import ZipFile

from httpio import SeekableHTTPFile
from urllib_passwords import configure_domain_password

scihub_credentials = None
if scihub_credentials:
    passwords = {
        "https://scihub.esa.int/": scihub_credentials
    }
    configure_domain_password(passwords)


class TestSeekableHTTPFile(TestCase):
    def test_text_file(self):
        url = "https://docs.python.org/3/library/io.html#module-io"
        name = "text.htm"
        f = SeekableHTTPFile(url, name, debug=True)
        f.seek(-200, io.SEEK_END)
        pos = f.tell()
        self.assertEqual(pos, f.content_length - 200)
        text = f.read(50)
        self.assertIsInstance(text, bytes)
        self.assertEqual(len(text), 50)
        self.assertEqual(name, f.name)

    def test_non_seekable(self):
        url = "https://github.com/kennethreitz/requests/archive/v2.8.1.zip"
        f = SeekableHTTPFile(url, debug=True)
        self.assertEqual(f.name, "requests-2.8.1.zip")
        self.assertFalse(f.seekable())
        with self.assertRaises(OSError):
            f.seek(5)

    def test_zip(self):
        url = "https://www.python.org/ftp/python/3.5.0/python-3.5.0-embed-amd64.zip"
        f = SeekableHTTPFile(url, debug=True)
        zf = ZipFile(f)
        zf.printdir()
        filelist = set(zf.namelist())
        self.assertIn("python.exe", filelist)
        pyenv = zf.read("pyvenv.cfg")
        self.assertEqual(pyenv.rstrip(), b"applocal = true")

    def test_scihub_product(self):
        if not scihub_credentials:
            self.skipTest("SciHub username and password must be provided for testing")
            return
        # One of the smallest files on SciHub
        url = "https://scihub.esa.int/dhus/odata/v1/Products('8dfa1139-6643-4e74-b16f-5226d438d7ed')/$value"
        f = SeekableHTTPFile(url, repeat_time=1, debug=True)
        zf = ZipFile(f)
        namelist = zf.namelist()
        print(namelist)
        target = next(filter(lambda x: x.endswith("manifest.safe"), namelist))
        manifest = zf.read(target)
        self.assertTrue(manifest.startswith(b'<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertTrue(len(manifest) > 100)
