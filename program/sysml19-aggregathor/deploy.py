# coding: utf-8
###
 # @file   deploy.py
 # @author Sébastien Rouault <sebastien.rouault@epfl.ch>
 #         Georgios Damaskinos <georgios.damaskinos@epfl.ch>
 #
 # @section LICENSE
 #
 # Copyright © 2018-2019 Sébastien ROUAULT.
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
 #
 # @section DESCRIPTION
 #
 # TF cluster automated deployment over SSH.
###

if __name__ != "__main__":
  raise RuntimeError("Script " + repr(__file__) + " is to be used as the main module only")

import argparse
import os
import signal
import socket
import subprocess
import sys
import time

# Special import scheme for stand-alone instances
try:
  import tools
  cluster_parse   = tools.cluster_parse
  cluster_parsers = tools.cluster_parsers
except Exception:
  import json
  cluster_parse   = lambda x: json.loads(x)
  cluster_parsers = ""

# ---------------------------------------------------------------------------- #
# Graceful termination

# Registered exit callbacks and calling
exit_callbacks = []
exit_pending   = False

def mark_exit(*args, **kwargs):
  """ Simply mark exit as pending.
  """
  global exit_pending
  exit_pending = True

def clean_exit(code, *args, **kwargs):
  """ Call all the exit callbacks, then exit.
  Args:
    code Return code
    ...  Arguments to forward to the callbacks
  """
  # Call registered callbacks
  global exit_callbacks
  for callback in exit_callbacks:
    callback(*args, **kwargs)
  # Actual exit
  exit(code)

# Signal handlers
signal.signal(signal.SIGINT, mark_exit)
signal.signal(signal.SIGTERM, mark_exit)

# ---------------------------------------------------------------------------- #
# Command line

# Description
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--cluster",
  type=str,
  required=True,
  help="Full cluster specification, JSON format: {\"<jobname>\": [\"hostname:port\", ...], ...}" + ("" if len(cluster_parsers) == 0 else ", or special value(s): " + cluster_parsers))
parser.add_argument("--deploy",
  action="store_true",
  default=False,
  help="Whether this instance must deploy the whole cluster through SSH")
parser.add_argument("--id",
  type=str,
  help="This node's role, format: <job>:<id>")
parser.add_argument("--nice",
  nargs="*",
  help="Make this process nice, or list of job(s) which tasks must maximize their respective niceness level")
parser.add_argument("--omit",
  action="store_true",
  default=False,
  help="Do not start the node's server instance, can be used only with '--id' and '--deploy'")

# ID parser
def parse_id(text):
  """ Parse and return the <job>:<id> string.
  Args:
    text String to parse
  Returns:
    This node's job name, this node's id
  """
  sep = text.rfind(":")
  if sep < -1:
    raise ValueError("Invalid ID format")
  nid = int(text[sep + 1:])
  if nid < 0:
    raise ValueError("Expected non-negative node ID")
  return text[:sep], nid

# Command line parsing and checks
args = parser.parse_args(sys.argv[1:])
cluster = cluster_parse(args.cluster)
cluster_repr = repr(cluster).replace("'", "\"")
nices = args.nice if args.nice is not None else []
for job in nices:
  if job not in cluster:
    print("\033[1;33mJob " + repr(job) + " does not appear in the cluster specification, hence cannot be nice\033[0m")
deploy = args.deploy
omit = args.omit
if args.id is None:
  if not deploy:
    raise RuntimeError("Nothing to do (no deployment and no node ID)")
  if omit:
    raise RuntimeError("Cannot omit starting the node's server instance if its identity is unknown")
  this_job, this_id = None, None
else:
  if omit and not deploy:
    raise RuntimeError("Nothing to do (no server start and no deployment)")
  this_job, this_id = parse_id(args.id)
  if this_job not in cluster or this_id >= len(cluster[this_job]):
    raise ValueError("Role is not in the specified cluster")
  be_nice = args.nice is not None and (args.nice == [] or this_job in args.nice)
del args

# ---------------------------------------------------------------------------- #
# (NFS-free) SSH deployment

source = None
def deploy_source():
  """ Lazy-load and return the source code of the current script.
  Returns:
    This script source code
  """
  global source
  if source is None:
    with open(__file__, "rb") as f:
      source = f.read()
  return source

def deploy_one(host, cluster, node_job, node_id):
  """ Deploy a cluster node through SSH.
  Args:
    host     Target host name
    cluster  Full cluster specification
    node_job Node's job name
    node_id  Node's task id
  """
  args = ["ssh", host, sys.executable]

  # Need to get path to TensorFlow if installed locally
  pythonpath=os.environ.get('PYTHONPATH','')
  syspaths=''
  syspaths_added=[]
  for pp in pythonpath.split(':'):
      if pp!='' and pp not in syspaths_added:
         syspaths+="sys.path.append('"+pp+"'); "
         syspaths_added.append(pp)

  handler = subprocess.Popen(args, stdin=subprocess.PIPE)
  exit_callbacks.append(lambda *args, **kwargs: handler.terminate())
  handler.stdin.write(("import sys; "+syspaths+" sys.argv = [\"\", \"--cluster\", " + repr(cluster_repr) + ", " + ("\"--nice\", " if node_job in nices else "") + "\"--id\", " + repr(node_job + ":" + str(node_id)) + "]; " + os.linesep).encode())
  handler.stdin.write(deploy_source())
  handler.stdin.close()

def deploy_all(cluster, this_job, this_id):
  """ Deploy all the given cluster through SSH, except this node if specified, register the exit handler.
  Args:
    cluster  Full cluster specification
    this_job This node's job name, that won't be deployed (None to deploy all)
    this_id  This node's task id
  """
  for node_job, hosts in cluster.items():
    for node_id in range(len(hosts)):
      if exit_pending:
        return
      if this_job and node_job == this_job and node_id == this_id: # Do not deploy (again) this node
        continue
      # Host name parsing
      host = hosts[node_id]
      hpos = host.find(":")
      if hpos < 0:
        raise ValueError("Invalid hostname:port format")
      host = host[:hpos]
      # Deploy node
      deploy_one(host, cluster, node_job, node_id)

# ---------------------------------------------------------------------------- #
# TensorFlow server

def server_as(cluster, node_job, node_id):
  """ Create and start a TF cluster server.
  Args:
    cluster  Full cluster specification
    this_job This node's job name
    this_id  This node's task id
  """
  if be_nice:
    os.nice(19)
  import tensorflow as tf
  cluster = tf.train.ClusterSpec(cluster)
  server  = tf.train.Server(cluster, job_name=this_job, task_index=this_id, start=True)
  print("\033[1;32m[" + node_job + ":" + str(node_id) + "] " + server.target.decode().replace("localhost", socket.gethostname()) + (" (nice)" if be_nice else "") + "\033[0m")

# ---------------------------------------------------------------------------- #
# Main

# Deploy if asked
if not exit_pending and deploy:
  deploy_all(cluster, this_job, this_id)

# Serve if asked
if not exit_pending and this_job is not None:
  if omit:
    print("\033[1;34m[" + this_job + ":" + str(this_id) + "] No server running\033[0m")
  else:
    server_as(cluster, this_job, this_id)

# Flush standard outputs
sys.stdout.flush()
sys.stderr.flush()

# Wait exit request
while not exit_pending:
  time.sleep(1)
  if os.getppid() <= 1:
    break

# Clean exit
clean_exit(0)
