#!/usr/bin/env python3

"""
Give corpus files a filename based on their contents and their rtl_433 output.
"""

import hashlib
import json
import os
import sys
import subprocess

def main():
    print('Corpus file naming application', file=sys.stderr)
    if len(sys.argv) != 3:
        print('Usage: {} RTL_BIN_PATH CORPUS_PATH'.format(sys.argv[0]), file=sys.stderr)
        return
    rtl_bin = sys.argv[1]
    corpus_path = sys.argv[2]
    print('Checking if rtl_433 binary is working and correct path is given', file=sys.stderr)
    res = subprocess.run([rtl_bin, '-V'], capture_output=True)
    if res.returncode == 0 or res.returncode == 1:
        print('rtl_433 bin ok', file=sys.stderr)
    else:
        print('Could not find rtl_433 binary', file=sys.stderr)
        return
  
    counter = 0
    for filename in os.listdir(corpus_path):
        newname = 'empty'
        filepath = corpus_path + filename
        with open(filepath, 'rb') as file:
            m = hashlib.sha256()
            filedata = file.readlines()
            for line in filedata:
                m.update(line)
            hash = m.hexdigest()

        res = subprocess.run([rtl_bin, '-G', '4', '-F', 'json', '-y', '@'+filepath], capture_output=True)
        try:
            text = res.stdout.decode('utf-8').rstrip()
        except UnicodeDecodeError as e:
            print(f"ERROR: Exception thrown while decoding text, {filepath}, {res.stdout}: {e}")
            text = ''
        if text == '':
            newname = 'no-output'
        else:
            try:
                line = text.splitlines()[0]
                data = json.loads(line)
                newname = data['model']
            except json.decoder.JSONDecodeError as e:
                # if a decode error happens, print the rtl_433 output and the error
                print(text, file=sys.stderr)
                print(e, file=sys.stderr)
                newname = 'json-decode-error'

        # replace /, they can't be in a filename
        newname_safe = newname.replace('/', '-')
        name = '{}-{}'.format(newname_safe, hash[0:16])
        #print(name)
        # Skip files that have this name already
        if name == filename:
            #print('Skipping', name, ', it already exists')
            continue
        os.rename(filepath, corpus_path + name)
        counter += 1
    print('Renamed {} files'.format(counter), file=sys.stderr)

if __name__ == '__main__':
    main()
