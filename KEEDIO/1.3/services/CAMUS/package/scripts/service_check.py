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

import os
from resource_management import *
from functools import partial
from utils import *
from camus import camus

class ServiceCheck(Script):


  def service_check(self, env):
    import params
    env.set_params(params)
    execute_camus = partial(execute_sudo_krb,user=params.smoke_user,principal=params.smoke_user,keytab=params.smoke_user_keytab)
    Logger.info("Sourcing /etc/profile.d/hadoop-env.sh")
    cmd=Popen('/bin/grep export  /etc/profile.d/hadoop-env.sh ',stdout=PIPE,stderr=PIPE,shell=True)
    out,err=cmd.communicate()
    Logger.info(out)
    Logger.info(err)
    # parsing the output
    listout=out.split('\n')
    listout.remove('')
    for line in listout:
         cmdlist=line.replace('=',' ').split(' ') 
         os.environ[cmdlist[1]]=cmdlist[2]

    Logger.info("The environment for camus execution:")
    Logger.info(os.environ)
    check_camus = [str(params.camus_local_home)+"/bin/run-camus-example.sh"]
    out,err,rc=execute_camus(check_camus)
    check_rc(rc,stdout=out,stderr=err)

if __name__ == "__main__":
  ServiceCheck().execute()