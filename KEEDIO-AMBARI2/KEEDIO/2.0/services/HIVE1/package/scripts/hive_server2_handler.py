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

import sys
from resource_management import *

from hive import hive

         
class HiveServerHandler(Script):
  def install(self, env):
    import params
    #self.install_packages(env)
    Package("hive")
    Package("hive-server2")
    
  def configure(self, env):
    import params
    env.set_params(params)
    hive(action='config',service='hive-server2')
    
  def start(self, env):
    self.configure(env)
    hive(action='start',service='hive-server2')
    
  def stop(self, env):
    hive(action='stop',service='hive-server2')

  def status(self, env):
    hive(action='status',service='hive-server2')
     
if __name__ == "__main__":
  HiveServerHandler().execute()