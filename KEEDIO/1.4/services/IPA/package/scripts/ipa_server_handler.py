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

from freeipa import freeipa

         
class FreeIPAHandler(Script):
  def install(self, env):
    self.install_packages(env)
    freeipa(action='install')
    freeipa(action='config')
    
  def configure(self, env):
    import params
    env.set_params(params)
    freeipa(action='config')
    
  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)
    freeipa(action='start')
    
  def stop(self, env):
    import params
    freeipa(action='stop')

  def status(self, env):
    freeipa(action='status')
     
if __name__ == "__main__":
  FreeIPAHandler().execute()
