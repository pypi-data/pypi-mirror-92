# Copyright (c) 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import shlex
import tempfile
import time
import uuid

from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging
import sys
import zmq

from shaker.engine import config
from shaker.engine import utils


LOG = logging.getLogger(__name__)


def poll_task(socket, agent_id):
    payload = {
        'operation': 'poll',
        'agent_id': agent_id,
    }
    LOG.debug('Polling task: %s', payload)
    socket.send_json(payload)
    res = socket.recv_json()
    LOG.debug('Received: %s', res)
    return res


def send_reply(socket, agent_id, result):
    message = {
        'operation': 'reply',
        'agent_id': agent_id,
    }
    message.update(result)

    LOG.debug('Sending reply: %s', message)
    socket.send_json(message)
    res = socket.recv_json()
    LOG.debug('Received: %s', res)
    return res


def run_command(command):
    command_stdout, command_stderr = None, None
    start = time.time()
    agent_dir = cfg.CONF.agent_dir

    if agent_dir:
        utils.mkdir_tree(agent_dir)

    if command['type'] == 'program':
        command_stdout, command_stderr = processutils.execute(
            *shlex.split(command['data']), check_exit_code=False)

    elif command['type'] == 'script':
        if 'agent_dir' in cfg.CONF:
            file_name = tempfile.mktemp(dir="%s" % agent_dir)
        else:
            file_name = tempfile.mktemp()

        with open(file_name, mode='w') as fd:
            fd.write(command['data'])
        LOG.debug('Stored script into %s', file_name)
        command_stdout, command_stderr = processutils.execute(
            *shlex.split('bash %s' % file_name), check_exit_code=False)

    else:
        command_stderr = 'Unknown command type : %s' % command['type']

    return dict(stdout=command_stdout, stderr=command_stderr,
                start=start, finish=time.time())


def time_now():
    return time.time()


def sleep(seconds):
    time.sleep(seconds)


def get_socket(context, endpoint):
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 0)
    if 'agent_socket_recv_timeout' in cfg.CONF:
        socket.setsockopt(zmq.RCVTIMEO, cfg.CONF.agent_socket_recv_timeout)
    if 'agent_socket_send_timeout' in cfg.CONF:
        socket.setsockopt(zmq.SNDTIMEO, cfg.CONF.agent_socket_send_timeout)
    socket.connect('tcp://%s' % endpoint)
    return socket


def work_act(socket, agent_id, agent_config):
    task = poll_task(socket, agent_id)
    start_at = task.get('start_at')

    if start_at:
        now = time_now()
        start_at_str = datetime.datetime.fromtimestamp(
            start_at).isoformat()

        if start_at > now:
            LOG.debug('Scheduling task at %s', start_at_str)
            sleep(start_at - now)
        else:
            LOG.warning('Scheduling in the past: %s', start_at_str)

    if task.get('operation') == 'execute':
        result = run_command(task.get('command'))
        send_reply(socket, agent_id, result)
        LOG.info('Finished executing task: %s', task)

    elif task.get('operation') == 'configure':
        if 'polling_interval' in task:
            agent_config['polling_interval'] = task.get('polling_interval')
            send_reply(socket, agent_id, {})
            LOG.info('Agent reconfigured: %s', agent_config)

    sleep(agent_config['polling_interval'])


def work(agent_id, endpoint, polling_interval=config.DEFAULT_POLLING_INTERVAL,
         ignore_sigint=False):
    LOG.info('Agent id is: %s', agent_id)
    LOG.info('Connecting to server: %s', endpoint)

    agent_config = dict(polling_interval=polling_interval)
    LOG.info('Agent config: %s', agent_config)

    if 'agent_socket_conn_retries' in cfg.CONF:
        socket_conn_retries = cfg.CONF.agent_socket_conn_retries
    else:
        socket_conn_retries = config.DEFAULT_SOCKET_CONN_RETRIES

    context = zmq.Context()
    socket = get_socket(context, endpoint)
    socket_retries_left = socket_conn_retries

    while True:
        try:
            work_act(socket, agent_id, agent_config)
            socket_retries_left = socket_conn_retries

        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                if ignore_sigint:
                    LOG.info('Got SIGINT, but configured to ignore it')
                else:
                    LOG.info('Process is interrupted')
                    sys.exit(3)
            elif isinstance(e, zmq.error.ZMQError):
                socket.close()
                socket_retries_left -= 1
                if socket_retries_left <= 0:
                    LOG.exception(e)
                    break
                LOG.warning('Socket reconnecting...')
                socket = get_socket(context, endpoint)
            else:
                LOG.exception(e)
                break

    socket.close()
    context.term()


def get_node_uuid():
    s = '%012x' % uuid.getnode()
    return ':'.join([s[i:i + 2] for i in range(0, len(s), 2)])


def main():
    utils.init_config_and_logging(config.COMMON_OPTS + config.AGENT_OPTS)

    endpoint = cfg.CONF.server_endpoint
    polling_interval = cfg.CONF.polling_interval
    agent_id = cfg.CONF.agent_id

    if not agent_id:
        agent_id = get_node_uuid()
        LOG.info('Using node uuid as agent_id: %s', agent_id)

    work(agent_id, endpoint, polling_interval)


if __name__ == "__main__":
    main()
