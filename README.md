# pyhttpio
Read files behind HTTP URLs as if they were local by adding seeking functionality to HTTPResponses. This is intended as a simple Python proof of concept.

Seeking is accomplished by manipulating the `range: bytes=xx-yy` HTTP header.

This functionality can be useful when handling large archives or images, where it allows a small file or some other portion of it to be easily extracted without needing to download the full thing. See  the test snippets in [`test_seekableHTTPFile.py`](./test_seekableHTTPFile.py) for examples.
