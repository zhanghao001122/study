#!/usr/bin/env python

from collections import defaultdict
from subprocess import Popen, PIPE
import sys
import json
import bisect
import os


role2ips = defaultdict(list)

try:
    process = Popen(['fuel', '--env', os.environ.get('CLUSTER_ID', ''), 'node'],
                    stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code != 0:
        print('err')
        sys.exit(0)
except:
    print('{}')
    sys.exit(0)

for line in output.split('\n')[2:]:
    if len(line.split('|')) != 10:
        continue
    [_, _, _, _, ip, _, roles, _, _, _] = line.split('|')
    ip = ip.strip()
    for role in roles.split(','):
        bisect.insort(role2ips[role.strip()], ip)

#result = json.dumps(role2ips)
#print role2ips
#print role2ips.keys()

try:
    os.mknod('hosts', 0644)
except:
    pass

file = open('hosts', 'w')
for key in role2ips.keys():
    group = '[' + key + ']'
    file.write(group)
    file.write('\n')
    for ip in role2ips[key]:
        file.write(ip)
        file.write('\n')
    file.write('\n')
file.close()

