#!/usr/bin/env python

import sys, os, datetime
from subprocess import call
from operator import itemgetter

BAK_DIR = "/zvol/bak/database/zabbix_pg"

def get_mtime(path):
    return os.stat(path).st_mtime

def do_pgdump(filename):
    cmd = ["sudo", "-u", "zabbix", "pg_dump", "-h", "127.0.0.1", "-p", "5151", "zabbix"]
    with open(filename, 'w') as outfile:
        retcode = call(cmd, stdout=outfile)
        if retcode != 0:
            print "Zabbix pg_dump FAILED! Return code: {}".format(retcode)
        else:
            print "Zabbix pg_dump completed successfully"

def main():
    newfilebasename = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")+".dmp"
    do_pgdump(os.path.join(BAK_DIR, newfilebasename))
    curr_files = os.walk(BAK_DIR).next()[2]
    if len(curr_files) > 2:
        file_times = {x:get_mtime(os.path.join(BAK_DIR, x)) for x in curr_files}
        oldfile = sorted(file_times.items(), key=itemgetter(1))[0][0]
        os.unlink(os.path.join(BAK_DIR, oldfile))
    else:
        print "FAIL: no new files in {} after do_pgdump!".format(BAK_DIR)


if __name__ == "__main__":
    main()
