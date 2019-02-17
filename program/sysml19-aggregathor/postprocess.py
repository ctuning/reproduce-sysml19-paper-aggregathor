#
# Convert raw output of the Caffe 'time' command
# to the CK timing format.
#
# Developers:
#   - Grigori Fursin, cTuning foundation / dividiti, 2016
#   - Anton Lokhmotov, dividiti, 2016-2017
#

import json
import os
import re
import sys

def ck_postprocess(i):
    ck=i['ck_kernel']

    rt=i['run_time']
    deps=i['deps']

    d={}

    env=i.get('env',{})

    rf1=rt.get('run_cmd_out1','') # stdout
    rf2=rt.get('run_cmd_out2','') # stderr

    lst=[]

    if os.path.isfile(rf1):
       r=ck.load_text_file({'text_file':rf1,'split_to_list':'yes'})
       if r['return']>0: return r
       lst+=r['lst']

    # Finding and unifying different characteristics
    for q in lst:
        j1=q.find('(perf)')
        if j1<0:
           j1=q.find('[perf]')
        if j1>=0:
           if 'perf' not in d:
              d['perf']=[]
           x=q[j1+6:].strip()
           j1=x.find(' ')
           if j1>=0:
              x=x[j1+1:].strip()
           d['perf'].append(x)

        j1=q.find('Step 10000: top1-X-acc =')
        if j1>=0:
           j2=q.find('(took',j1+1)
           if j2>=0:
              j3=q.find(' s)',j2+1)
              if j3>=0:
                 d['top1-x-acc']=q[j1+24:j2-1].strip()
                 d['top1-x-acc-time']=q[j2+5:j3].strip()
                 d['post_processed']='yes'


    # Embedding to the CK pipeline

    rr={}
    rr['return']=0
    if d.get('post_processed','')=='yes':
        ck.out('  Success!)')
        # Save to file.
        r=ck.save_json_to_file({'json_file':'tmp-ck-timer.json', 'dict':d})
        if r['return']>0: return r
    else:
        rr['return']=1
        rr['error']='failed to find the \'Total Time\' string in Caffe output'

    return rr

# Do not add anything here!
