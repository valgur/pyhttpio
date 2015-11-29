# pyhttpio
Read files behind HTTP URLs as if they were local by adding seeking functionality to HTTPResponses. Intended as a simple Python proof of concept.

Seeking is accomplished through the 'range: bytes=xx-yy' HTTP header.