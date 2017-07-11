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
from yaml_utils import escape_yaml_propetry
import sys
import time
from ambari_agent.AgentException import AgentException
from subprocess import *

def storm(service=None,action=None):
  if action == "config":
    import params
    Directory(params.storm_log_dir,
            owner=params.storm_user,
            group=params.user_group,
            mode=0775,
            create_parents=True
    )

    Directory([params.storm_local_dir, params.conf_dir],
            owner=params.storm_user,
            group=params.user_group,
            create_parents=True
    )

    configurations = params.config['configurations']['storm-site']
  
    File(format("{conf_dir}/storm.yaml"),
       content=Template(
                        "storm.yaml.j2", 
                         extra_imports=[escape_yaml_propetry], 
                        configurations = configurations),
       owner=params.storm_user,
       group=params.user_group
    )
    #if params.has_ganglia_server:
    #   File('/etc/jmxtrans/config/jmxtrans.config',
    #      content=Template('jmxtrans.j2')
    #   )


    if params.has_metric_collector:
      File(format("{conf_dir}/storm-metrics2.properties"),
        owner=params.storm_user,
        group=params.user_group,
        content=Template("storm-metrics2.properties.j2")
       )

    # Remove symlinks. They can be there, if you doing upgrade from HDP < 2.2 to HDP >= 2.2
      Link(format("{storm_lib_dir}/ambari-metrics-storm-sink.jar"),
         action="delete")
    # On old HDP 2.1 versions, this symlink may also exist and break EU to newer versions
      Link("/usr/lib/storm/lib/ambari-metrics-storm-sink.jar", action="delete")

      sink_jar = params.metric_collector_sink_jar

      Execute(format("ln -s {sink_jar} {storm_lib_dir}/ambari-metrics-storm-sink.jar"),
              not_if=format("ls {storm_lib_dir}/ambari-metrics-storm-sink.jar"),
              only_if=format("ls {sink_jar}")
      )  


    File(format("{conf_dir}/storm-env.sh"),
      owner=params.storm_user,
      content=InlineTemplate(params.storm_env_sh_template)
    )
    File(format("{conf_dir}/storm_env.ini"),
      owner=params.storm_user,
      content=StaticFile('storm_env.ini')
    )
    File('/etc/monit.conf',content=StaticFile('monit.conf'))
    monit_status = Popen(["service","monit","status"])
    out,err=monit_status.communicate()
    rc=monit_status.returncode
    if rc == 0:
      executed = Popen(["service","monit","reload"])
    else:
      executed = Popen(["service","monit","start"])

  if service is not None:
    if  service != "storm-drpc" and service != "storm-logviewer" and service != "jmxtrans" and (action == "start" or action == "stop"):
      cmd=Popen(['monit',action,service,'-v'],stdout=PIPE,stderr=PIPE)
      time.sleep(30)
    else:
      cmd=Popen(['service',service,action],stdout=PIPE,stderr=PIPE)

    from functions import check_rc
    out,err=cmd.communicate()
    rc=cmd.returncode
    Logger.info("Storm Nimbus service %s: %s" % (action, cmd.returncode == 0))
   
    check_rc(rc,stdout=out,stderr=err)

    

'''
Finds minimal real user UID
'''
def _find_real_user_min_uid():
  with open('/etc/login.defs') as f:
    for line in f:
      if line.strip().startswith('UID_MIN') and len(line.split()) == 2 and line.split()[1].isdigit():
        return int(line.split()[1])
  raise AgentException ("Unable to find UID_MIN in file /etc/login.defs. Expecting format e.g.: 'UID_MIN    500'")  
