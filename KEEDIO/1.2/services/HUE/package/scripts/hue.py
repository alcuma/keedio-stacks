#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
import sys
import os

from subprocess import *

def hue(service=None,action=None):

  if action == "initdb":
    import params 
    cmd=Popen(['/usr/lib/hue/build/env/bin/hue','syncdb','--noinput'],stdout=PIPE,stderr=PIPE)
    out,err=cmd.communicate()
    Logger.info("Hue installation: sync db")
    Logger.info(out)
    Logger.info(err)
    cmd=Popen(['/usr/lib/hue/build/env/bin/hue','migrate'],stdout=PIPE,stderr=PIPE)
    out,err=cmd.communicate()
    Logger.info("Hue installation: migrate tables")
    Logger.info(out) 
    Logger.info(err) 
    
    Logger.info("Hue installation: Installation of kafka-hue")
    os.chmod('/usr/lib/hue/tools/app_reg/app_reg.py',0755)
    os.chdir('/usr/lib/hue/apps')
    cmd=Popen(['../tools/app_reg/app_reg.py','--install','kafka','--relative-paths'],stdout=PIPE,stderr=PIPE)
    out,err=cmd.communicate()
    Logger.info(out)
    Logger.info(err)
    Logger.info("Hue installation: Installation of storm-hue")
    cmd=Popen(['../tools/app_reg/app_reg.py','--install','storm','--relative-paths'],stdout=PIPE,stderr=PIPE)
    out,err=cmd.communicate()
    Logger.info(out)
    Logger.info(err)

  if action == "config":
    import params
    #configurations = params.config['configurations']['spark']
    File(format(params.hue_conf_dir+"hue.ini"),
       content=Template("hue.ini.j2"),
       owner="root",
       group="root"
    )

  if action == "start" or action == "stop":
    cmd=Popen(['service','hue',action],stdout=PIPE,stderr=PIPE)
    out,err=cmd.communicate()
    rc=cmd.returncode
    Logger.info("Hue service %s: %s" % (action, cmd.returncode == 0)) 

  if action == "status":
      from utils import check_rc
      cmd=Popen(['service','hue',action],stdout=PIPE,stderr=PIPE)
      out,err=cmd.communicate()
      rc=cmd.returncode
      Logger.info(rc)
      Logger.info("Hue service %s: %s" % (action, cmd.returncode == 0))

      check_rc(rc,stdout=out,stderr=err)

  