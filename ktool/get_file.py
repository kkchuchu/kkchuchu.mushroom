import sys
import subprocess
import asyncio

import sh
import argcomplete
import argparse


SERVER=['storage']
PRE_COMMAND=['docker', 'exec']
AFTER_COMMAND=['/usr/local/hadoop/bin/hadoop', 'fs', '-copyToLocal']
DEST=['/home/root/work/workspace']

"""
Retrieval file from local docker id:storage to workspace
"""

async def get_file_from_hdfs(source):
    process = subprocess.Popen(PRE_COMMAND + SERVER + AFTER_COMMAND + source + DEST, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    stdout, stderr = process.communicate()
    print(stderr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='+', help='the source location in hdfs')
    argcomplete.autocomplete(parser)
    args = parser.parse_args()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_file_from_hdfs(args.source))
    loop.close()
