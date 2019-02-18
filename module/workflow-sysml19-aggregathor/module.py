#
# Collective Knowledge (Workflow to automate validation of results from the SysML'19 paper: "AGGREGATHOR: Byzantine Machine Learning")
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# run workflow

def run(i):
    """
    Input:  {
              (cmd_key)    - local-mnist, local-mnist-attack or local-cifar10
              (aggregator) - if not specified, use the list of ['averaged-median', 'krum-co', 'krum-py', 'average', 'median', 'krum-tf', 'average-nan', 'bulyan-co', 'bulyan-py']
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import shutil
    import copy

    gar=cfg['aggregators'] # See .cm/meta.json of this CK module 

    # If output is to console (i.e. interactive mode), pass it to all further modules
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    # check customization
    cmd_key=i.get('cmd_key','')
    if cmd_key=='': cmd_key='local-mnist'

    if i.get('aggregator','')!='':
       gar=[i['aggregator']]

    pcur=os.getcwd()
    pres=os.path.join(pcur, 'results')

    resolved_deps={}

    # Loop through all aggregators
    str=''
    for agg in sorted(gar):
        ck.out('**************************************************************')

        ck.out('* CMD_KEY:    '+cmd_key)
        ck.out('* Aggregator: '+agg)

        ck.out('')

        str+='****************************************************************\n'
        str+='* CMD_KEY:    '+cmd_key+'\n'
        str+='* Aggregator: '+agg+'\n\n'

        if not os.path.isdir(pres):
           os.makedirs(pres)

        # How to set CK to platform generic-linux-dummy if there is a problem with sudo on GRID5000:
        #r=ck.access({'action':'detect',
        #             'module_uoa':'platform',
        #             'platform_init_uoa':'generic-linux-dummy',
        #             'update_platform_init':'yes',
        #             'out':oo})
        #if r['return']>0: return r

        # Set program pipeline
        copy_resolved_deps=copy.deepcopy(resolved_deps)

        pipeline={
                   'data_uoa':'sysml19-aggregathor',
                   'cmd_key':cmd_key,
                   'env':{'AGGREGATOR':agg},
                   'no_state_check':'yes',
                   'dependencies':copy_resolved_deps
                 }

        # Run program pipeline
        ii={'action':'autotune',
            'module_uoa':'pipeline',
            'data_uoa':'program',

            'iterations': 1,
            'repetitions': 3, # statistical repetitions of the same program pipeline

            'record':'yes',
            'record_failed':'yes',

            'record_params':{
                'search_point_by_features':'yes'
            },

            'tags':'syml19,experiments,raw,aggregathor',
            'meta':{},

            'record_repo':'local',
            'record_uoa':'sysml19-aggregathor-'+cmd_key+'-'+agg,

            'pipeline':pipeline,
            'out':oo
           }
        r=ck.access(ii)
        if r['return']>0: return r

        ck.save_json_to_file({'json_file':'/tmp/xyz1.json','dict':r})

        # If first time, get resolved deps and record platform and env
        if len(resolved_deps)==0:
           os.system('ck detect platform > '+os.path.join(pres,'ck-platform.log'))
           os.system('ck show env > '+os.path.join(pres,'ck-env.log'))

           resolved_deps=copy.deepcopy(r.get('dependencies',{}))

        # Copy output
        cur_dir=r.get('state',{}).get('cur_dir','')
        p1=os.path.join(cur_dir, 'stdout.log')
        p2=os.path.join(cur_dir, 'stderr.log')

        if os.path.isfile(p1):
           px1=os.path.join(pres, cmd_key+'-'+agg+'-stdout.log')
           shutil.copyfile(p1,px1)

           # Load file and add numbers (accuracy, perf) to str
           r=ck.load_text_file({'text_file':p1, 'split_to_list':'yes'})
           if r['return']>0: return r
           lst=r['lst']

           for l in lst:
               if '(test)' in l or '(perf)' in l:
                  j=l.find('[RUNNER]')
                  if j>=0:
                     l=l[j:]
                  str+=l.strip()+'\n'

        if os.path.isfile(p2):
           px2=os.path.join(pres, cmd_key+'-'+agg+'-stderr.log')
           shutil.copyfile(p2,px2)

    # Record general info
    pt=os.path.join(pres, 'results.txt')
    r=ck.save_text_file({'text_file':pt, 'string':str})
    if r['return']>0: return r

    # Archive results (can reply them)
    ck.out('**************************************************************')

    p=os.path.join(pres, 'ck-results.zip')

    if os.path.isfile(p):
       os.remove(p)

    ck.out('Archiving experimental results: '+p)
    ck.out('')

    os.chdir(pres)

    ii={'action':'zip',
        'cid':'local:experiment:sysml19-aggregathor-*',
        'archive_name':'ck-results.zip',
        'overwrite':'yes',
        'out':oo}
    r=ck.access(ii)
    if r['return']>0: return r

    return {'return':0}
