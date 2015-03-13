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
from utils import check_rc
from subprocess import *

def zkfc(action=None, format=False):
  if action == "configure":
    File("/etc/monit.d/hadoop-hdfs-zkfc",
      content=StaticFile("monit.d_hadoop-hdfs-zkfc"))
    File("/etc/monit.conf",
      content=StaticFile("monit.conf"))
 
  #First check monit is running and start if not
  executed = Popen(["service","monit","status"])
  executed.communicate()
  rc = executed.returncode
  if rc > 0 or action=="configure":
    executed = Popen(["service","monit","restart"])
    executed.communicate()

  if action == "start" or action == "stop":
    executed = Popen(["monit",action,"hadoop-hdfs-zkfc"],stdout=PIPE,stderr=PIPE)
    out,err = executed.communicate()
    rc = executed.returncode
    check_rc(rc,out,err)

  if action == "status":
    executed = Popen(["service","hadoop-hdfs-zkfc",action],stdout=PIPE,stderr=PIPE)
    out,err = executed.communicate()
    rc = executed.returncode
    check_rc(rc,out,err)


