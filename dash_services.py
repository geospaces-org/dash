#!/usr/bin/env python 

#*** DO NOT EDIT - GENERATED FROM tseries/notebooks/tseries_services.ipynb ****

import sys, os,  glob, logging, datetime
from  mangorest.mango import webapi
from colabexts import utils as colabexts_utils
import pandas as pd

sys.path.append("../..")

MBASE  = "/opt/data/data/dashboards/"
logger = logging.getLogger( "geoapp" )

#---------------------------------------------------------------------------------    
@webapi("/dashboard/save_dashboard")
def save_dashboard( name, contents, **kwargs):
    name = name or "default"
    if (name.endswith(".json")):
        name = name[:-5]
        
    dst = f"{MBASE}/{name}.json"
    dstd= os.path.dirname(dst)
    if not os.path.exists(dstd ):
        os.makedirs(dstd)
    
    with open(dst, "w") as f:
        f.write(contents.strip())

    return f"Saved {dst}"    
#---------------------------------------------------------------------------------    
@webapi("/dashboard/get_dashboard")
def get_dashboard( name, **kwargs):
    if (name.endswith(".json")):
        name = name[:-5]
    dst = f"{MBASE}/{name}.json"
    if not os.path.exists(os.path.dirname(dst) ):
        os.makedirs(dst)
    
    ret = open(dst, "r").read()
    return ret  
#------------------------------------------------------------------------------
@webapi("/dashboard/delete_dashboard")
def delete_dashboard(name="", **kwargs):
    dst = f"{MBASE}/{name}.json"
    if ( not os.path.exists(dst) ):
        return "OK {dst} does not exist!!"
    os.remove(dst)

    return f"Deleted {dst}."
#------------------------------------------------------------------------------
@webapi("/dashboard/getall_dashboards")
def getAllDashboards( nrows=10000, patt='*.json', **kwargs):
    
    files = glob.glob(f"{MBASE}{patt}")
    files.sort(key=os.path.getmtime, reverse=True)

    ret = {
        "name": "dashboards",
        "columns": ["name"],
        "values": [[f[len(MBASE):]] for f in files][0:nrows]
    }
    return ret
#------------------------------------------------------------------------------
@webapi("/dashboard/testdash")
def testdash( t=2, **kwargs):
    # take a long time to respond back
    import time
    t = max( 2, min( int(t), 10))
    time.sleep( int(t) )
    return f"Slept for {t} seconds :)"
#------------------------------------------------------------------------------
def _getSystemStats(request=None, **kwargs):
    import platform,  socket, psutil,  random

    kb,mb, gb = float(1024), float(1024 * 1024), float( 1024 * 1024 * 1024)

    memTotal       = int(psutil.virtual_memory()[0]/gb)
    memFreeGB        = int(psutil.virtual_memory()[1]/gb)
    memUsedGB        = int(psutil.virtual_memory()[3]/gb)
    memFreeMB        = int(psutil.virtual_memory()[1]/mb)
    memUsedMB        = int(psutil.virtual_memory()[3]/mb)
    memPercent     = int(memUsedGB/memTotal*100)
    storageTotal   = int(psutil.disk_usage('/')[0]/gb)
    storageUsed    = int(psutil.disk_usage('/')[1]/gb)
    storageFree    = int(psutil.disk_usage('/')[2]/gb)
    storagePercent = int(storageUsed/storageTotal*100)
    info           = "CPU"
    ts             = int(datetime.datetime.now().timestamp()*1000) + 1000

    out=f''' {{
        time            : {ts},
        cpu_count       : {os.cpu_count()},
        host            : "{socket.gethostname()}",
        System          : "{platform.system(),platform.machine()}",
        memoryUnits     : "GiB",
        memory          : {memTotal}, 
        memFreeGB       : {memFreeGB},
        memUsedGB       : {memUsedGB},
        memFreeMB       : {memFreeMB},
        memUsedMB       : {memUsedMB},
        memory_prcnt    : {memPercent},
        n_processes     : {len(psutil.pids())},
        load_avg_1min   : {round(os.getloadavg()[0],2)},
        load_avg_5min   : {round(os.getloadavg()[1],2)},
        load_avg_15min  : {round(os.getloadavg()[2],2)},
        lat             : {   39.5199452 + random.random() } ,
        lon             : { -104.9390802 + random.random() } ,
        altitude        : { 10000 + random.random() * 10   } ,  # altitude in in feet
        temperature     : {random.random() * 10 + 32}

    }}'''
    p = colabexts_utils.parsej(out, **kwargs)
    df = pd.DataFrame([p])
    return df
#------------------------------------------------------------------------------
SYSTEM_INFO_DF = None
@webapi("/dashboard/system_info")
def system_info( request, **kwargs):
    global SYSTEM_INFO_DF
    df = _getSystemStats(request, **kwargs)
    if (SYSTEM_INFO_DF is None):
        SYSTEM_INFO_DF = df
    else:
        SYSTEM_INFO_DF = pd.concat([df, SYSTEM_INFO_DF])

    SYSTEM_INFO_DF = SYSTEM_INFO_DF[-500:] # just keep last 500 rows for debugging
    ret = {
        "name" : "system_info",
        'columns': [c for c in SYSTEM_INFO_DF.columns],
        'values' : SYSTEM_INFO_DF.values.tolist()        
    }
    return ret

#------------------------------------------------------------------------------
@webapi("/dashboard/sample_data")
def sample_data( request, **kwargs):
    from random import random 
    n = kwargs.get("n", 1)
    
    ts = int(datetime.datetime.now().timestamp()*1000) 
    ret = {
        "name": "sample_data",
        "columns": ["time"] + [ f"v{i}" for i in range(n)],
        "values":  [[ts+i*1000] + [random() for j in range(n)] for i in range(100)]
    }
    return ret
