from mtdata import log
from mtdata.entry import Entry

from dataclasses import dataclass
from typing import TextIO, List
import abc
from collections import defaultdict

class Reporter(abc.ABC):

    @abc.abstractmethod
    def report(self, entries: List[Entry], out: TextIO, **kwargs):
        raise NotImplementedError()

@dataclass
class PlainReporter(Reporter):
    """Writes plain text output"""
    field_sep: str = '\t'
    rec_sep = '\n'
    full: bool = False


    def report(self, entries, out: TextIO):
        mem = defaultdict()

        for i, ent in enumerate(entries):
            out.write(ent.format(delim=self.field_sep))
            out.write(self.rec_sep)
            if self.full:
                out.write(ent.cite or "CITATION_NOT_LISTED")
                out.write(self.rec_sep)
                out.write(self.rec_sep)
