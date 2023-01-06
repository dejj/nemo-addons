#!/usr/bin/python3
from collections import defaultdict

# Provide columns for sorting filename-tagged media files, without changing the ID3 tags etc.
# 
#
# Copy this file to
#    /usr/share/nemo-python/extensions/
# or:
#    ~/.local/share/nemo-python/extensions/
#
# Other examples, see:
# - https://github.com/linuxmint/nemo-extensions/blob/master/nemo-python/examples/block-size-column.py
# - https://github.com/linuxmint/nemo-extensions/blob/master/nemo-media-columns/nemo-media-columns.py
#
# CAVEAT: python will let you define multiple 'class ColumnExtension', and Nemo will repeat the column of one of them

import os
import urllib.parse

from gi.repository import GObject, Nemo

class ColumnExtensionForTags(GObject.GObject, Nemo.ColumnProvider, Nemo.InfoProvider, Nemo.NameAndDescProvider):


    def __init__(self):
        # Initializes global dictionary-of-dictionaries for word frequency-per-folder.
        # Top-level key will be the folder path.
        # 2nd level key will be the word extraced from the filename.
        self.freq_dict = defaultdict(lambda: defaultdict(lambda: 0))
        self.files_seen = dict()
        pass

    def get_columns(self):
        return (
            Nemo.Column(name="NemoPython::at_1_column"  ,attribute="at_1",label=("@1"),description="Get the 1st at-prefixed part"),
            Nemo.Column(name="NemoPython::at_2_column"  ,attribute="at_2",label=("@2"),description="Get the 2nd at-prefixed part"),
            Nemo.Column(name="NemoPython::dollar_1_column",attribute="dollar_1",label=("$1"),description="Get the 1st dollar-prefixed part"),
            Nemo.Column(name="NemoPython::dollar_2_column",attribute="dollar_2",label=("$2"),description="Get the 2nd dollar-prefixed part"),
            Nemo.Column(name="NemoPython::hash_1_column",attribute="hash_1",label=("#1"),description="Get the 1st hashtagged part"),
            Nemo.Column(name="NemoPython::hash_2_column",attribute="hash_2",label=("#2"),description="Get the 2nd hashtagged part"),
            Nemo.Column(name="NemoPython::name_2_column",attribute="name_2",label=("Name2"),description="Get the name after first space"),
            Nemo.Column(name="NemoPython::name_3_column",attribute="name_3",label=("Name3"),description="Get the name after second space"),
            Nemo.Column(name="NemoPython::freq_1_column",attribute="freq_1",label=("freq1"),description="Most frequent word wrt. all names in folder"),
            Nemo.Column(name="NemoPython::freq_2_column",attribute="freq_2",label=("freq2"),description="2nd-most frequent word wrt. all names in folder"),
            Nemo.Column(name="NemoPython::freq_at_1_column",attribute="freq_at_1",label=("f@1"),description="Most frequent at-prefixed part wrt. all names in folder"),
            Nemo.Column(name="NemoPython::freq_at_2_column",attribute="freq_at_2",label=("f@2"),description="2nd-most frequent at-prefixed wrt. all names in folder"),
            Nemo.Column(name="NemoPython::freq_at_3_column",attribute="freq_at_3",label=("f@3"),description="3rd-most frequent at-prefixed wrt. all names in folder"),
            Nemo.Column(name="NemoPython::freqs_column",attribute="freqs",label=("freqs"),description="Frequencies of word part wrt. all names in folder"),
        )

    def update_file_info(self, file):
        if file.get_uri_scheme() != 'file':
            return

        # Obtains absolute filename by stripping 'file://'
        file_uri = file.get_uri()
        filename = urllib.parse.unquote(file_uri[7:])

        # Splits into path and actual filename, including suffix.
        path, tail = os.path.split(filename)

        # Pretends there is a space before the last dot, so the suffix doesn't stick to the last tag.
        parts_around_dots = tail.split('.') 
        prefix = '.'.join(parts_around_dots[:-1])
        suffix = '.'.join(parts_around_dots[-1:])
        # Rebuilds the filename, in case the file has no suffix, but there is a dot in the middle of the name.
        tail_rebuilt = prefix + " " + suffix

        # Extracts all the words from the filename.
        parts = tail_rebuilt.split(' ')

        # Splits off anything before the first space.
        name2 = ' '.join(parts[1:2])
        name3 = ' '.join(parts[2:3])

        at         = [x for x in parts if x.startswith('@')]
        dollared   = [x for x in parts if x.startswith('$')]
        hashtagged = [x for x in parts if x.startswith('#')]
        
        local_dict = self.freq_dict[str(path)]
        # Adds all words from the filename to the frequency dictionary.
        if filename not in self.files_seen:
            self.files_seen[filename] = True
            for word in parts:
                local_dict[word] += 1

        # Gets all keys from frequency dictionary for local folder and sorts them by frequency.
        # Nemo will make sure to pass through all files in a folder before evaluating this.
        local_freqs = sorted(((freq,word) for (word,freq) in local_dict.items() if word in parts and len(word) > 1), reverse=True)

        freq_at = [word for (freq,word) in local_freqs if word.startswith('@')]

        file.add_string_attribute('at_1', show(at[0:1]))
        file.add_string_attribute('at_2', show(at[1:2]))
        file.add_string_attribute('dollar_1', show(dollared[0:1]))
        file.add_string_attribute('dollar_2', show(dollared[1:2]))
        file.add_string_attribute('hash_1', show(hashtagged[0:1]))
        file.add_string_attribute('hash_2', show(hashtagged[1:2]))
        file.add_string_attribute('name_2', str(name2))
        file.add_string_attribute('name_3', str(name3))
        file.add_string_attribute('freqs', str(local_freqs))
        file.add_string_attribute('freq_at_1', show(freq_at[0:1]))
        file.add_string_attribute('freq_at_2', show(freq_at[1:2]))
        file.add_string_attribute('freq_at_3', show(freq_at[2:3]))
        # FIXME: some may fail
        file.add_string_attribute('freq_1', '%s(%d)'%(local_freqs[1][1], local_freqs[1][0]))
        file.add_string_attribute('freq_2', '%s(%d)'%(local_freqs[2][1], local_freqs[2][0]))
        

def show(ary):
    return '\u3000' if not ary else str(' '.join(ary))