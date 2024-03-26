#!/bin/bash

set -o pipefail -e
export PRELAUNCH_OUT="/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/prelaunch.out"
exec >"${PRELAUNCH_OUT}"
export PRELAUNCH_ERR="/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/prelaunch.err"
exec 2>"${PRELAUNCH_ERR}"
echo "Setting up env variables"
export JAVA_HOME=${JAVA_HOME:-"/usr/lib/jvm/java-11-openjdk-amd64"}
export HADOOP_COMMON_HOME=${HADOOP_COMMON_HOME:-"/usr/local/revisedJQF/v8/hadoop-3.3.6"}
export HADOOP_HDFS_HOME=${HADOOP_HDFS_HOME:-"/usr/local/revisedJQF/v8/hadoop-3.3.6"}
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-"/usr/local/revisedJQF/v8/hadoop-3.3.6/etc/hadoop"}
export HADOOP_YARN_HOME=${HADOOP_YARN_HOME:-"/usr/local/revisedJQF/v8/hadoop-3.3.6"}
export HADOOP_HOME=${HADOOP_HOME:-"/usr/local/revisedJQF/v8/hadoop-3.3.6"}
export PATH=${PATH:-"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}
export HADOOP_TOKEN_FILE_LOCATION="/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/appcache/application_1701312551309_0035/container_1701312551309_0035_01_000001/container_tokens"
export CONTAINER_ID="container_1701312551309_0035_01_000001"
export NM_PORT="38033"
export NM_HOST="ed761ad59d44"
export NM_HTTP_PORT="8042"
export LOCAL_DIRS="/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/appcache/application_1701312551309_0035"
export LOCAL_USER_DIRS="/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/"
export LOG_DIRS="/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001"
export USER="root"
export LOGNAME="root"
export HOME="/home/"
export PWD="/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/appcache/application_1701312551309_0035/container_1701312551309_0035_01_000001"
export LOCALIZATION_COUNTERS="521709,0,4,0,265"
export JVM_PID="$$"
export NM_AUX_SERVICE_mapreduce_shuffle="AAA0+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
export APPLICATION_WEB_PROXY_BASE="/proxy/application_1701312551309_0035"
export SHELL="/bin/bash"
export CLASSPATH="$PWD:$HADOOP_CONF_DIR:$HADOOP_COMMON_HOME/share/hadoop/common/*:$HADOOP_COMMON_HOME/share/hadoop/common/lib/*:$HADOOP_HDFS_HOME/share/hadoop/hdfs/*:$HADOOP_HDFS_HOME/share/hadoop/hdfs/lib/*:$HADOOP_YARN_HOME/share/hadoop/yarn/*:$HADOOP_YARN_HOME/share/hadoop/yarn/lib/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/etc/hadoop:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/common/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/common/lib/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/hdfs/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/hdfs/lib/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/mapreduce/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/mapreduce/lib/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/yarn/*:/usr/local/revisedJQF/v8/hadoop-3.3.6/share/hadoop/yarn/lib/*:job.jar/*:job.jar/classes/:job.jar/lib/*:$PWD/*"
export APP_SUBMIT_TIME_ENV="1701315353874"
export LD_LIBRARY_PATH="$PWD:$HADOOP_COMMON_HOME/lib/native"
export MALLOC_ARENA_MAX="4"
echo "Setting up job resources"
mkdir -p jobSubmitDir
ln -sf -- "/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/appcache/application_1701312551309_0035/filecache/12/job.split" "jobSubmitDir/job.split"
mkdir -p jobSubmitDir
ln -sf -- "/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/appcache/application_1701312551309_0035/filecache/10/job.splitmetainfo" "jobSubmitDir/job.splitmetainfo"
ln -sf -- "/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/appcache/application_1701312551309_0035/filecache/13/job.xml" "job.xml"
ln -sf -- "/home/hadoop3/hadoop/tmp/nm-local-dir/usercache/root/appcache/application_1701312551309_0035/filecache/11/job.jar" "job.jar"
ln -sf -- "/home/hadoop3/hadoop/tmp/nm-local-dir/filecache/52/_partition.lst" "_partition.lst"
echo "Copying debugging information"
# Creating copy of launch script
cp "launch_container.sh" "/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/launch_container.sh"
chmod 640 "/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/launch_container.sh"
# Determining directory contents
echo "ls -l:" 1>"/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/directory.info"
ls -l 1>>"/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/directory.info"
echo "find -L . -maxdepth 5 -ls:" 1>>"/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/directory.info"
find -L . -maxdepth 5 -ls 1>>"/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/directory.info"
echo "broken symlinks(find -L . -maxdepth 5 -type l -ls):" 1>>"/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/directory.info"
find -L . -maxdepth 5 -type l -ls 1>>"/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/directory.info"
echo "Launching container"
exec /bin/bash -c "$JAVA_HOME/bin/java -Djava.io.tmpdir=$PWD/tmp -Dlog4j.configuration=container-log4j.properties -Dyarn.app.container.log.dir=/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001 -Dyarn.app.container.log.filesize=0 -Dhadoop.root.logger=INFO,CLA -Dhadoop.root.logfile=syslog  -Xmx1024m org.apache.hadoop.mapreduce.v2.app.MRAppMaster 1>/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/stdout 2>/usr/local/revisedJQF/v8/hadoop-3.3.6/logs/userlogs/application_1701312551309_0035/container_1701312551309_0035_01_000001/stderr "
