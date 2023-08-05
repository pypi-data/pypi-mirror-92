from tinydb import TinyDB, Query
from typing import List, Dict
from datetime import datetime
from .singleton import SingletonMeta
from .tinydb_exceptions import *
import dtos
from multiprocessing import Lock


class HostTinyDbWrapper(metaclass=SingletonMeta):
    """
    Wrapper class for TinyDB within CRM system to manage host information
    """

    def __init__(self, db_path: str, access_lock: Lock) -> None:
        # create db
        self.db = TinyDB(db_path, sort_keys=True, indent=2, separators=(',', ': '))
        # create hosts table
        self.hosts = self.db.table('hosts')
        # create lock
        self.lock = access_lock
        # create timing-format
        self.time_format = '%H:%M:%S %d-%m-%Y'

    def insert_host(self, info: 'dtos.HostInfo') -> bool:
        """
        Insert a new host into db
        :param info: an instance of HostInfo
        :return: True if success, False otherwise
        """
        self.lock.acquire()
        try:
            is_inserted = False
            ports = []
            for p in info.ports:
                ports.append({"daemon": p.daemon, "port": p.port})

            self.hosts.insert({"hostname": info.hostname,
                               "inet_addr": info.inet_addr,
                               "ports": ports,
                               "type": info.type.name,
                               "latest_recv": datetime.now().strftime(self.time_format)})
            is_inserted = True
        except Exception as err:
            raise InsertError('Cannot insert new host {}'.format(str(info)), err)
        finally:
            self.lock.release()
            return is_inserted

    def check_host_existence(self, hostname: str) -> bool:
        """
        Check whether a host with certain hostname is already included in the hosts table
        :param hostname: hostname of the host need to check
        :return: True if included, False otherwise
        """
        self.lock.acquire()
        hosts = self.hosts.all()
        is_found = False
        for host in hosts:
            if host['hostname'] == hostname:
                is_found = True
        self.lock.release()
        return is_found

    def get_all_hostnames_by_type(self, host_type: 'dtos.HostType') -> []:
        """
        Get all hostnames of a certain type
        :param host_type: type of host we want to filter
        :return: list of hostnames
        """
        hostnames = []
        self.lock.acquire()
        try:
            hosts = self.hosts.all()

            if hosts:
                for h in hosts:
                    if dtos.HostType.__dict__[h['type']] == host_type:
                        hostnames.append(h['hostname'])
        except Exception as err:
            raise GetError('Cannot find hostname with type={}'.format(str(host_type)), err)
        finally:
            self.lock.release()
            return hostnames

    def get_host_by_hostname(self, hostname: str) -> dtos.HostInfo:
        """
        Get info of a host by its hostname
        :param hostname: hostname of a worker/controller
        :return: HostInfo instance
        """
        self.lock.acquire()
        try:
            host = Query()
            record = self.hosts.search(host.hostname == hostname)
            host_info = None
            if record:
                port_infos = []
                for info in record[0]["ports"]:
                    port_infos.append(dtos.PortInfo(info["daemon"], info["port"]))

                host_info = dtos.HostInfo(record[0]["hostname"],
                                             record[0]["inet_addr"],
                                             port_infos,
                                             # https://stackoverflow.com/questions/41407414/convert-string-to-enum-in-python
                                             dtos.HostType.__dict__[record[0]["type"]])
            else:
                raise Exception('Not found.')
        except Exception as err:
            raise GetError('Cannot find host by hostname={}'.format(hostname), err)
        finally:
            self.lock.release()
            return host_info

    def get_daemon_by_name(self, hostname: str, daemon: str) -> dtos.PortInfo:
        """
        Get daemon information of a worker/collector by its hostname
        :param hostname: hostname of a host
        :param daemon: name of daemon
        :return: an instance of PortInfo
        """
        self.lock.acquire()
        try:
            host = Query()
            record = self.hosts.search(host.hostname == hostname)[0]
            port_info = None
            if record:
                for info in record["ports"]:
                    if info["daemon"] == daemon:
                        port_info = dtos.PortInfo(info["daemon"], info["port"])

        except Exception as err:
            raise GetError('Cannot get daemon name={} of host with hostname={}'.format(daemon, hostname), err)
        finally:
            self.lock.release()
            return port_info

    def update_host_metrics(self, hostname, metrics: List[Dict]) -> bool:
        """
        Update metrics information of a host with a certain hostname
        :param hostname: hostname of host
        :param metrics: list of PortInfo
        :return: True if succeed, False otherwise
        """
        self.lock.acquire()
        try:
            host = Query()
            self.hosts.upsert({'metrics': metrics},
                              host.hostname.matches(hostname))

        except Exception as err:
            raise UpdateError('Cannot update metrics: {} of host with hostname={}'.format(metrics, hostname), err)
        finally:
            self.lock.release()
            return True

    def update_host_heartbeat(self, hostname: str) -> bool:
        """
        Update latest_update information of a host with a certain hostname
        :param hostname: hostname of host
        :return: True if success, UpdateError otherwise
        """
        self.lock.acquire()
        try:
            host = Query()
            self.hosts.update({'latest_recv': datetime.now().strftime(self.time_format)},
                              host.hostname.matches(hostname))

        except Exception as err:
            raise UpdateError('Cannot update latest_recv of host with hostname={}'.format(hostname), err)
        finally:
            self.lock.release()
            return True

    def check_heartbeat(self, hostname: str, current_time, max_interval: int) -> bool:
        """
        Check whether latest_update information of a host with a certain hostname is overdue
        :param hostname: hostname of host
        :param current_time: time of the moment of checking
        :param max_interval: maximum seconds allowed between check
        :return:
        """
        self.lock.acquire()
        try:
            host = Query()
            record = self.hosts.search(host.hostname == hostname)[0]
            is_within_range = False
            if record:
                latest_update = datetime.strptime(record['latest_recv'], self.time_format)
                difference = current_time - latest_update

                is_within_range = int(difference.total_seconds()) <= max_interval

        except Exception as err:
            raise HeartbeatError('Cannot check heartbeat of host with hostname={}'.format(hostname), err)
        finally:
            self.lock.release()
            return is_within_range


class QueryCriteriaTinyDbWrapper(metaclass=SingletonMeta):
    """
    Wrapper class for TinyDB within CRM system to manage criteria of resource usage queries
    """

    def __init__(self, db_path: str, access_lock: Lock) -> None:
        # create db
        self.db = TinyDB(db_path, sort_keys=True, indent=2, separators=(',', ': '))
        # create query table
        self.criteria_info = self.db.table('criteria_info')
        # create lock
        self.lock = access_lock
        # create timing-format
        self.time_format = '%H:%M:%S %d-%m-%Y'

    def insert_queryinfo(self, sys_type: str, job: str, info: List['dtos.FilterInfo']) -> bool:
        """
        Insert a FilterInfo to db
        :param sys_type: type of the system (simulation/production)
        :param job: name of a prometheus job
        :param info: a list of instance of FilterInfo
        :return: True if success, False otherwise
        """
        self.lock.acquire()
        try:
            type_query_info = self._check_info_existence(sys_type, job)
            is_inserted = False
            # if type_query_info is not existed
            if not type_query_info:
                filters = []
                for item in info:
                    filters.append({'category': item.category, 'criteria': item.criteria})

                self.criteria_info.insert({'type': sys_type,
                                           'job': job,
                                           'filters': filters})
                is_inserted = True
            # in case host_query_info, we add/update the category if needed
            else:
                query = Query()
                record = self.criteria_info.search(query.type == sys_type and query.job == job)
                old_filters = record[0]['filters']
                for item_info in info:
                    # if category of new FilterInfo (item_info) is already included in the database
                    if item_info.category in [d['category'] for d in old_filters]:
                        for item_filter in old_filters:
                            if item_info.category == item_filter['category']:
                                # now we compare each criterion of item_info and item_filter
                                for crit_info in item_info.criteria:
                                    # add with comparing field_name (unique check)
                                    if crit_info['field_name'] not in [d['field_name'] for d in
                                                                       item_filter['criteria']]:
                                        item_filter['criteria'].append(crit_info)
                                    else:
                                        if crit_info['field_value'] not in [d['field_value'] for d in
                                                                            item_filter['criteria']]:
                                            item_filter['criteria'].append(crit_info)

                    # else, we add the whole new category and all of its criteria
                    else:
                        old_filters.append({'category': item_info.category, 'criteria': item_info.criteria})

                self.criteria_info.update({'filters': old_filters},
                                          query.type.matches(sys_type) and query.job.matches(job))
                is_inserted = True

        except Exception as err:
            raise InsertError('Cannot insert FilterInfo of {}-{} to db'.format(sys_type, job), err)
        finally:
            self.lock.release()
            return is_inserted

    def _check_info_existence(self, sys_type: str, job: str) -> bool:
        """
        Check whether FilterInfo with certain type & job is already included in the query_info table
        :param sys_type: type of system (simulation/production)
        :param job: name of a prometheus job
        :return: True if included, False otherwise
        """
        infos = self.criteria_info.all()
        for info in infos:
            if info['type'] == sys_type and info['job'] == job:
                return True
        return False

    def get_criteria_by_type_job_category(self, sys_type: str, job: str, category: str) -> List[Dict[str, str]]:
        """
        Get the list of FilterInfo of a worker using hostname, job, and category values
        :param sys_type: type of system (simulation/production)
        :param job: name of a prometheus job
        :param category: cpu/memory/disk/disk_io/network_io
        :return: List of FilterInfo's criteria
        """
        self.lock.acquire()
        query_infos = self.criteria_info.all()
        criteria = None
        for info in query_infos:
            if info['type'] == sys_type and info['job'] == job:
                for item in info['filters']:
                    if item['category'] == category:
                        criteria = item['criteria']
        self.lock.release()
        return criteria

    def get_categories_by_type_job(self, sys_type: str, job: str) -> List[str]:
        """
        Get the list of all category of FilterInfo of a worker using hostname and job values
        :param sys_type: type of system (simulation/production)
        :param job: name of a prometheus job of the worker
        :return: List of names of FilterInfo's categories
        """
        self.lock.acquire()
        categories = []
        query_infos = self.criteria_info.all()
        for info in query_infos:
            if info['type'] == sys_type and info['job'] == job:
                for item in info['filters']:
                    categories.append(item['category'])
        self.lock.release()
        return categories
