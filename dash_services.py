#!/usr/bin/env python 

#*** DO NOT EDIT - GENERATED FROM tseries/notebooks/tseries_services.ipynb ****

import sys, os,  glob, logging
from  mangorest.mango import webapi

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
