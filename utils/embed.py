# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os, string, sys


if sys.version_info.major >= 3:
    def escape(s): return s.encode('unicode-escape').decode()
else:
    def escape(s): return s.encode('string-escape')


_, text_file, output_dir, variable = sys.argv


if not os.path.exists(output_dir):
    os.mkdir(output_dir)


header = [
    '#pragma once',
    'extern const char* %s;' % variable,
]


source = [
    'const char* %s =' % variable
]

with open(text_file) as f:
    for line in f:
        new_line = ''

        for char in line:
            if char not in string.printable:
                new_line += '\\%03o' % ord(char)
            else:
                new_line += escape(char)

        source.append('"%s"' % new_line)

source.append(';')


outputs = {
    'source.c': source,
    'source.h': header,
}


for output_file, contents in outputs.items():
    with open(os.path.join(output_dir, output_file), 'w') as f:
        f.write('\n'.join(contents))
