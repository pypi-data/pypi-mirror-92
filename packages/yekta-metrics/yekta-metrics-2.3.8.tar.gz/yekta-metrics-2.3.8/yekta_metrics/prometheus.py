import glob
import os
import re
import platform
import threading
import logging
from time import sleep
from prometheus_client import start_http_server, push_to_gateway, \
    Enum, Counter, Gauge, Summary, Histogram, CollectorRegistry, multiprocess
from prometheus_client.exposition import basic_auth_handler
from prometheus_client import values as prometheus_values
from .config import *

logger = logging.getLogger('METRICS')


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def get_custom_metric(metric_type):
    class CustomMetric(metric_type):
        def __init__(self, name, *args, **kwargs):
            name = "_".join((METRICS_APP_NAME, camel_to_snake(name))).lower()
            super().__init__(name, *args, **kwargs)

    return CustomMetric


class PrometheusClient:
    registry = CollectorRegistry()
    counter = get_custom_metric(Counter)
    gauge = get_custom_metric(Gauge)
    histogram = get_custom_metric(Histogram)
    summary = get_custom_metric(Summary) if METRICS_ALLOW_USING_SUMMARY else None

    @staticmethod
    def pushgateway_auth_handler(url, method, timeout, headers, data):
        return basic_auth_handler(url, method, timeout, headers, data,
                                  METRICS_PUSH_GATEWAY_USERNAME, METRICS_PUSH_GATEWAY_PASSWORD)

    @staticmethod
    def _make_multi_process_share_dir_ready(share_dir):
        # Create share dir if not exist
        if not os.path.exists(share_dir):
            os.makedirs(share_dir)

        if METRICS_MULTI_PROCESS_CLEAR_SHARE_DIR:
            # Wipe old metrics
            files = glob.glob(f'{share_dir}/*')
            for f in files:
                os.remove(f)

        if 'prometheus_multiproc_dir' not in os.environ or os.environ['prometheus_multiproc_dir'] != share_dir:
            raise Exception(f"Please set env variable 'prometheus_multiproc_dir' to value {share_dir}")

    @staticmethod
    def _is_uwsgi_env():
        try:
            import uwsgi
            return True
        except ImportError:
            return False

    @staticmethod
    def _is_first_uwsgi_worker():
        import uwsgi
        return uwsgi.worker_id() == 1

    def __init__(self):
        try:
            if not METRICS_ENABLE:
                return

            metrics_mode = Enum('metrics_send_mode', 'Metrics Send Mode', states=['push', 'pull'])
            metrics_mode.state(METRICS_MODE.lower())

            assert METRICS_MULTI_PROCESS_MODE != (
                    METRICS_MODE == 'PUSH'), 'Can\'t use multiprocess mode with pushgateway'

            if METRICS_MULTI_PROCESS_MODE:
                share_dir = f'{METRICS_MULTI_PROCESS_SHARE_DIR}/{METRICS_APP_NAME}/{METRICS_MULTI_PROCESS_TYPE}'

                # TODO: fix gunicorn
                if not self._is_uwsgi_env() or (self._is_uwsgi_env() and self._is_first_uwsgi_worker()):
                    self._make_multi_process_share_dir_ready(share_dir)

                if self._is_uwsgi_env():
                    import uwsgi
                    prometheus_values.ValueClass = prometheus_values.MultiProcessValue(process_identifier=uwsgi.worker_id)

                multiprocess.MultiProcessCollector(self.registry)

            if METRICS_MODE == 'PULL':
                if not self._is_uwsgi_env() or (self._is_uwsgi_env() and self._is_first_uwsgi_worker()):
                    start_http_server(METRICS_SERVER_PORT, registry=self.registry)
                    logging.info(f'HTTP server listening on port {METRICS_SERVER_PORT}')
            elif METRICS_MODE == 'PUSH':
                def push_metrics():
                    while True:
                        logging.info(
                            f'Push metrics to {METRICS_PUSH_GATEWAY_URL} [interval={METRICS_PUSH_GATEWAY_INTERVAL}s]')
                        push_to_gateway(
                            gateway=METRICS_PUSH_GATEWAY_URL,
                            job=METRICS_PUSH_GATEWAY_JOB,
                            registry=self.registry,
                            handler=self.pushgateway_auth_handler,
                            grouping_key={
                                'app': METRICS_APP_NAME,
                                'instance': platform.node(),
                            }
                        )
                        sleep(METRICS_PUSH_GATEWAY_INTERVAL)

                metrics_push_interval = Gauge('metrics_push_interval', 'Metrics Push Interval')
                metrics_push_interval.set(METRICS_PUSH_GATEWAY_INTERVAL)

                assert METRICS_PUSH_GATEWAY_INTERVAL > METRICS_PUSH_GATEWAY_MIN_INTERVAL, 'Push interval is too small'
                threading.Thread(target=push_metrics).start()
            else:
                logger.error('BAD METRICS MODE. (only support PUSH or PULL values)')
        except Exception as e:
            logger.error('ERR: ' + str(e))
