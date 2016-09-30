#!/usr/bin/env python
# Copyright 2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Usage: ./cleanup_maintenance.py

Clean up boxes that should no longer be marked as 'draining' or 'down' for
maintenance. Also cleanup the associated dynamic reservations.
"""
import argparse
import logging
import sys

from paasta_tools.mesos_maintenance import get_draining_hosts
from paasta_tools.mesos_maintenance import get_hosts_forgotten_down
from paasta_tools.mesos_maintenance import get_hosts_forgotten_draining
from paasta_tools.mesos_maintenance import reserve_all_resources
from paasta_tools.mesos_maintenance import undrain
from paasta_tools.mesos_maintenance import unreserve_all_resources
from paasta_tools.mesos_maintenance import up
from paasta_tools.mesos_tools import get_slaves


log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='Cleans up forgotten maintenance cruft.')
    args = parser.parse_args()
    return args


def cleanup_forgotten_draining():
    """Clean up hosts forgotten draining"""
    log.debug("Cleaning up hosts forgotten draining")
    undrain(hostnames=get_hosts_forgotten_draining())


def cleanup_forgotten_down():
    """Clean up hosts forgotten down"""
    log.debug("Cleaning up hosts forgotten down")
    up(hostnames=get_hosts_forgotten_down())


def unreserve_all_resources_on_non_draining_hosts():
    """Unreserve all resources on non-draining hosts"""
    log.debug("Unreserving all resources on non-draining hosts")
    slaves = get_slaves()
    hostnames = map((lambda slave: slave['hostname']), slaves)
    draining_hosts = get_draining_hosts()
    non_draining_hosts = list(set(hostnames) - set(draining_hosts))
    unreserve_all_resources(hostnames=non_draining_hosts)


def reserve_all_resources_on_draining_hosts():
    """Reserve all resources on draining hosts"""
    log.debug("Reserving all resources on draining hosts")
    reserve_all_resources(hostnames=get_draining_hosts())


def cleanup_maintenance():
    log.debug("Cleaning up maintenance cruft")
    parse_args()

    cleanup_forgotten_draining()
    cleanup_forgotten_down()
    unreserve_all_resources_on_non_draining_hosts()
    reserve_all_resources_on_draining_hosts()


if __name__ == "__main__":
    if cleanup_maintenance():
        sys.exit(0)
    sys.exit(1)
