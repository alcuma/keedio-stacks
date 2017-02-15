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

from ambari_commons.constants import AMBARI_SUDO_BINARY
from resource_management.libraries.functions.version import format_stack_version, compare_versions
from resource_management.core.system import System
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions import default, format
from resource_management.libraries.functions.expect import expect

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
sudo = AMBARI_SUDO_BINARY

hdp_stack_version = str(config['hostLevelParams']['stack_version'])
#hdp_stack_version = format_hdp_stack_version(hdp_stack_version)
#Keedio:reduced to allow for different versioning
stack_is_hdp22_or_further = hdp_stack_version != "" and compare_versions(hdp_stack_version, '1.0') >= 0
agent_stack_retry_on_unavailability = config['hostLevelParams']['agent_stack_retry_on_unavailability']
agent_stack_retry_count = expect("/hostLevelParams/agent_stack_retry_count", int)

keedio_stack_version = str(config['hostLevelParams']['stack_version']) 

#users and groups
hbase_user = config['configurations']['hbase-env']['hbase_user']
smoke_user =  config['configurations']['cluster-env']['smokeuser']
gmetad_user = config['configurations']['gangliaui-env']["gmetad_user"]
gmond_user = config['configurations']['gangliaui-env']["gmond_user"]
tez_user = config['configurations']['tez-env']["tez_user"]

user_group = config['configurations']['cluster-env']['user_group']
proxyuser_group = default("/configurations/hadoop-env/proxyuser_group","users")

hdfs_log_dir_prefix = config['configurations']['hadoop-env']['hdfs_log_dir_prefix']

# repo templates
repo_rhel_suse =  config['configurations']['cluster-env']['repo_suse_rhel_template']
repo_ubuntu =  config['configurations']['cluster-env']['repo_ubuntu_template']
repodisable=[]
repoenable=[]

#hosts
hostname = config["hostname"]
ambari_server_hostname = config['clusterHostInfo']['ambari_server_host'][0]
rm_host = default("/clusterHostInfo/rm_host", [])
slave_hosts = default("/clusterHostInfo/slave_hosts", [])
oozie_servers = default("/clusterHostInfo/oozie_server", [])
hcat_server_hosts = default("/clusterHostInfo/webhcat_server_host", [])
hive_server_host =  default("/clusterHostInfo/hive_server_host", [])
hbase_master_hosts = default("/clusterHostInfo/hbase_master_hosts", [])
hs_host = default("/clusterHostInfo/hs_host", [])
jtnode_host = default("/clusterHostInfo/jtnode_host", [])
namenode_host = default("/clusterHostInfo/namenode_host", [])
zk_hosts = default("/clusterHostInfo/zookeeper_hosts", [])
ganglia_server_hosts = default("/clusterHostInfo/gangliaui_server_hosts", [])
storm_server_hosts = default("/clusterHostInfo/nimbus_hosts", [])
falcon_host =  default('/clusterHostInfo/falcon_server_hosts', [])

has_spacewalk_client = False
has_spacewalk_client = 'spacewalk' in config['configurations']


gpgcheck=0
spacewalk_timeout=180
if has_spacewalk_client:
    spacewalk_server = config['configurations']['spacewalk']['spacewalk_server']    
    spacewalk_certificate = config['configurations']['spacewalk']['spacewalk_certificate']    
    activation_key = config['configurations']['spacewalk']['activation_key']    
    spacewalk_pub_url = config['configurations']['spacewalk']['spacewalk_pub_url']
    gpgcheck=0 
    if  config['configurations']['spacewalk']['gpgcheck']:
         gpgcheck=1
    else: 
         gpgcheck=0
    spacewalk_timeout = default("/configurations/spacewalk/spacewalk_timeout",[180])

has_sqoop_client = 'sqoop-env' in config['configurations']
has_namenode = not len(namenode_host) == 0
has_hs = not len(hs_host) == 0
has_resourcemanager = not len(rm_host) == 0
has_slaves = not len(slave_hosts) == 0
has_oozie_server = not len(oozie_servers)  == 0
has_hcat_server_host = not len(hcat_server_hosts)  == 0
has_hive_server_host = not len(hive_server_host)  == 0
has_hbase_masters = not len(hbase_master_hosts) == 0
has_zk_host = not len(zk_hosts) == 0
has_ganglia_server = not len(ganglia_server_hosts) == 0
has_storm_server = not len(storm_server_hosts) == 0
has_falcon_server = not len(falcon_host) == 0
has_tez = 'tez-site' in config['configurations']

is_namenode_master = hostname in namenode_host
is_jtnode_master = hostname in jtnode_host
is_rmnode_master = hostname in rm_host
is_hsnode_master = hostname in hs_host
is_hbase_master = hostname in hbase_master_hosts
is_slave = hostname in slave_hosts
if has_ganglia_server:
  ganglia_server_host = ganglia_server_hosts[0]

hbase_tmp_dir = "/tmp/hbase-hbase"

#security params
security_enabled = config['configurations']['cluster-env']['security_enabled']

#java params
#java_home = config['hostLevelParams']['java_home']
java_home = "/usr/lib/jvm/jre"
artifact_dir = format("{tmp_dir}/AMBARI-artifacts/")
#jdk_name = default("/hostLevelParams/jdk_name", None) # None when jdk is already installed by user
jdk_name="java-1.7.0-openjdk.x86_64"
jce_policy_zip = default("/hostLevelParams/jce_name", None) # None when jdk is already installed by user
jce_location = config['hostLevelParams']['jdk_location']
jdk_location = config['hostLevelParams']['jdk_location']
ignore_groupsusers_create = default("/configurations/cluster-env/ignore_groupsusers_create", False)
host_sys_prepped = default("/hostLevelParams/host_sys_prepped", False)

smoke_user_dirs = format("/tmp/hadoop-{smoke_user},/tmp/hsperfdata_{smoke_user},/home/{smoke_user},/tmp/{smoke_user},/tmp/sqoop-{smoke_user}")
if has_hbase_masters:
  hbase_user_dirs = format("/home/{hbase_user},/tmp/{hbase_user},/usr/bin/{hbase_user},/var/log/{hbase_user},{hbase_tmp_dir}")
#repo params
repo_info = config['hostLevelParams']['repo_info']
service_repo_info = default("/hostLevelParams/service_repo_info",None)