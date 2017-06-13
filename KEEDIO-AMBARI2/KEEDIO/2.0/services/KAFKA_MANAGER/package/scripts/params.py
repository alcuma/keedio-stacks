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

# from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
from kazoo.client import KazooClient
from time import sleep
import kazoo

# exclude_packages=[]
config = Script.get_config()
zookeeper_server_hosts = str(default("/configurations/kafka-manager-properties/zookeeper.connect", None))
kafka_manager_hosts = default("/clusterHostInfo/kafka_manager_hosts", [])
log_dirs = default("/configurations/kafka-manager-properties/log.dirs", "")

kafka_manager_conf = default("/configurations/kafka-manager-properties", [])

# else:
#  exclude_packages.append('jmxtrans')
hostname = None
if config.has_key('hostname'):
    hostname = str(config['hostname'])

znode_kafka_path = str(default("/configurations/kafka-manager-env/znode_path", "/ambari/kafka-manager"))
kafka_manager_id = None

zk = KazooClient(hosts=zookeeper_server_hosts)
zk.start()

lock = zk.Lock("/kafka-manager-lock", hostname)
lock.acquire(timeout=60)

if zk.exists(znode_kafka_path + '/' + hostname):
    kafka_manager_id = int(zk.get(znode_kafka_path + '/' + hostname)[0])
else:
    kafka_manager_id = int(
        zk.create(znode_kafka_path + '/ids/', sequence=True, value=hostname, makepath=True).rsplit('/', 1)[1])
    zk.create(znode_kafka_path + '/' + hostname, value=str(kafka_manager_id), makepath=True)
lock.release()
zk.stop()
