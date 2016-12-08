import re
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open
import commands
import os


class OrgEmacsReader(BaseReader):
    enabled = True
    file_extensions = ['org']

    def read(self, filename):
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
                content = "\n".join(text[i:])
                break
        content="\"#+OPTIONS: toc:nil\n"+str(content)+"\""
        status,content=commands.getstatusoutput("emacs -Q --script %s/getContent.el %s"%(os.path.split(os.path.realpath(__file__))[0],content))
        return content, metadata

def add_reader(readers):
    for ext in OrgEmacsReader.file_extensions:
        readers.reader_classes[ext] = OrgEmacsReader

def register():
    signals.readers_init.connect(add_reader)
