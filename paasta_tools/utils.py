from datetime import datetime as dt

import clog
import staticconf


DEPLOY_PIPELINE_NON_DEPLOY_STEPS = (
    'itest',
    'security-check',
    'performance-check',
    'push-to-registry'
)


def get_git_url(service):
    """Get the git url for a service. Assumes that the service's
    repo matches its name, and that it lives in services- i.e.
    if this is called with the string 'test', the returned
    url will be git@git.yelpcorp.com:services/test.git.

    :param service: The service name to get a URL for
    :returns: A git url to the service's repository"""
    return 'git@git.yelpcorp.com:services/%s.git' % service


def configure_log():
    clog_config_path = "/nail/srv/configs/clog.yaml"
    staticconf.YamlConfiguration(clog_config_path, namespace='clog')


def _now():
    return str(dt.now())


def format_log_line(cluster, instance, line):
    """Accepts a string 'line'.

    Returns an appropriately-formatted dictionary which can be serialized to
    JSON for logging and which contains 'line'.
    """
    now = _now()
    return {
        'timestamp': now,
        'cluster': cluster,
        'instance': instance,
        'message': line,
    }


def get_log_name_for_service(service_name):
    return 'stream_paasta_%s' % service_name


def _log(service_name, cluster, instance, line):
    """This expects someone (currently the paasta cli main()) to have already
    configured the log object. We'll just write things to it.
    """
    line = format_log_line(cluster, instance, line)
    line = str(line)
    log_name = get_log_name_for_service(service_name)
    clog.log_line(log_name, line)
