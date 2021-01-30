#!/usr/bin/python3

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
                
        )

    def update_file_info(self, file):
        if file.get_uri_scheme() != 'file':
            return

        # obtain absolute filename by stripping file://
        filename = urllib.parse.unquote(file.get_uri()[7:])

        head, tail = os.path.split(filename)

        # pretend there is a space before the last dot, so the suffix doesn't stick to the last tag
        prefix = '.'.join(tail.split('.')[:-1])
        suffix = '.'.join(tail.split('.')[-1:])
        tail_rebuilt = prefix + " " + suffix


        parts = tail_rebuilt.split(' ')

        # split off anything before the first space
        name2 = ' '.join(parts[1:2])
        name3 = ' '.join(parts[2:3])

        at         = [x for x in parts if x.startswith('@')]
        dollared   = [x for x in parts if x.startswith('$')]
        hashtagged = [x for x in parts if x.startswith('#')]
        

        file.add_string_attribute('at_1', show(at[0:1]))
        file.add_string_attribute('at_2', show(at[1:2]))
        file.add_string_attribute('dollar_1', show(dollared[0:1]))
        file.add_string_attribute('dollar_2', show(dollared[1:2]))
        file.add_string_attribute('hash_1', show(hashtagged[0:1]))
        file.add_string_attribute('hash_2', show(hashtagged[1:2]))
        file.add_string_attribute('name_2', str(name2))
        file.add_string_attribute('name_3', str(name3))
        

def show(ary):
    return str(' '.join(ary))