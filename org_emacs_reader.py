#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import re
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open
import commands
from bs4 import BeautifulSoup

class OrgEmacsReader(BaseReader):
    enabled = True
    file_extensions = ['org']

    def getstatusoutput(self, cmd):
        """Return (status, output) of executing cmd in a shell."""
        import sys
        mswindows = (sys.platform == "win32")
        import os
        if not mswindows:
            cmd = '{ ' + cmd + '; }'
        pipe = os.popen(cmd + ' 2>&1', 'r')
        text = pipe.read()
        sts = pipe.close()
        if sts is None: sts = 0
        if text[-1:] == '\n': text = text[:-1]
        return sts, text

    def read(self, filename):
        print(filename)
        with pelican_open(filename) as fp:
            text = list(fp.splitlines())

        metadata = {}
        for i, line in enumerate(text):
            meta_match = re.match(r'^#\+([a-zA-Z]+):(.*)', line)
            if meta_match:
                name = meta_match.group(1).lower()
                value = meta_match.group(2).strip()
                metadata[name] = self.process_metadata(name, value)
            else:
                break
        import sys
        mswindows = (sys.platform == "win32")
        import os
        if not mswindows:
            status,content=commands.getstatusoutput("emacs -Q --script %s/getContent.el %s"%(os.path.split(os.path.realpath(__file__))[0],filename))
        else:
            status,content=self.getstatusoutput("emacs -Q --script %s %s"%(os.path.join(os.path.split(os.path.realpath(__file__))[0],"getContent.el"),filename))
        soup = BeautifulSoup(content, 'html.parser')
        if soup.find(id="table-of-contents"):
            soup.find(id="table-of-contents").extract()
        content=soup.prettify()
        h_level=range(2,6)
        for n in reversed(h_level):
            content=content.replace("<h"+str(n),"<h"+str(n+1))
            content=content.replace("</h" + str(n), "</h" + str(n + 1))
        return content,metadata

def add_reader(readers):
    for ext in OrgEmacsReader.file_extensions:
        readers.reader_classes[ext] = OrgEmacsReader

def register():
    signals.readers_init.connect(add_reader)
