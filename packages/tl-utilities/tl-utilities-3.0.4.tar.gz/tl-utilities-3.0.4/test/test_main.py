import os
import pathlib

from utilities import *
from dtos import *
from datetime import datetime
import yaml
from uuid import uuid4
import jsonpickle
import multiprocessing


def test_routine_checking_heartbeat(db_manager: 'HostTinyDbWrapper', interval: int):
    try:
        all_hostnames = db_manager.get_all_hostnames_by_type(HostType.WORKER)
        disconnected_hosts = []
        now = datetime.now()
        for hostname in all_hostnames:
            if not db_manager.check_heartbeat(hostname, now, interval):
                disconnected_hosts.append(hostname)

        print(disconnected_hosts)
    except HeartbeatError or GetError as err:
        print(err)


def test_check_heartbeat(db_manager: 'HostTinyDbWrapper', hostname: str, interval: int):
    try:
        result = db_manager.check_heartbeat(hostname, datetime.now(), interval)

        if result:
            print("Still good.")
        else:
            print("Need to update.")
    except HeartbeatError as err:
        print(err)


def test_update_heartbeat(db_manager: 'HostTinyDbWrapper', hostname: str):
    try:
        db_manager.update_host_heartbeat(hostname)
        host = db_manager.get_host_by_hostname(hostname)
        print("Latest info: {}".format(host))
    except UpdateError as err:
        print(err)


def test_get_host(db_manager: 'HostTinyDbWrapper', hostname: str):
    try:
        host = db_manager.get_host_by_hostname(hostname)
        print(host)
    except GetError as err:
        print(err)


def test_insert_hosts(db_manager: 'HostTinyDbWrapper', hostname: str, inet_addr: str,
                      ports: ['PortInfo'], hosttype: 'HostType'):
    try:
        host = HostInfo(hostname, inet_addr, ports, hosttype)
        result = db_manager.insert_host(host)
        if result:
            print("Insert {} to db successfully.".format(host))

    except InsertError as err:
        print(err)


def test_insert_queryinfo(db_manager: 'QueryCriteriaTinyDbWrapper'):
    node_cpu_filter_info = FilterInfo('cpu', [{'field_name': 'mode', 'field_value': 'idle', 'regex': '='}])
    node_disk_filter_info = FilterInfo('disk', [{'field_name': 'mountpoint', 'field_value': '/', 'regex': '='}])
    node_disk_io_filter_info = FilterInfo('disk_io',
                                          [{'field_name': 'device', 'field_value': '^.*sda.*$', 'regex': '=~'}])
    node_net_filter_info = FilterInfo('network_io', [{'field_name': 'device', 'field_value': '^wlp.*$', 'regex': '=~'}])

    cadvisor_cpu_filter_info = FilterInfo('cpu', [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_mem_filter_info = FilterInfo('memory', [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_disk_filter_info = FilterInfo('disk', [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_disk_io_filter_info = FilterInfo('disk_io',
                                              [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])
    cadvisor_network_io_filter_info = FilterInfo('network_io',
                                                 [{'field_name': 'id', 'field_value': '/docker/.+', 'regex': '=~'}])

    # insert FilterInfo to db
    db_manager.insert_queryinfo('simulation', 'nodeexporter',
                                [node_cpu_filter_info, node_disk_filter_info,
                                 node_disk_io_filter_info, node_net_filter_info])

    node_mem_filter_info = FilterInfo('memory', [{'field_name': 'mode', 'field_value': 'swap', 'regex': '=~'}])
    node_newcpu_filter_info = FilterInfo('cpu', [{'field_name': 'mode', 'field_value': '^.*sys.*$', 'regex': '!~'}])

    db_manager.insert_queryinfo('simulation', 'nodeexporter',
                                [node_newcpu_filter_info, node_mem_filter_info])

    db_manager.insert_queryinfo('simulation', 'cadvisor',
                                [cadvisor_cpu_filter_info, cadvisor_mem_filter_info,
                                 cadvisor_disk_filter_info, cadvisor_disk_io_filter_info,
                                 cadvisor_network_io_filter_info])


def main():
    access_lock = multiprocessing.Lock()
    # create db
    db = QueryCriteriaTinyDbWrapper('criteria_db.json', access_lock)
    test_insert_queryinfo(db)
    #main_path = str(pathlib.Path(__file__).parent.absolute())
    #with open(os.path.join(main_path, 'config.yaml'), 'r') as f:
    #    try:
    #        cfg = yaml.safe_load(f)
    #    except yaml.YAMLError as exc:
    #        print(exc)

    # debug
    # print(cfg)

    #container_configs = container_convert_yaml_to_json(cfg['architectd']['metric_exporters']['production']['containers'],
    #                                                   '3.8')

    #print(container_configs)


if __name__ == '__main__':
    main()
