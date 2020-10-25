#!/usr/bin/env python
# encoding: utf-8

import platform
import datetime
import psutil
import socket
import re
import sys
import uuid
import time
import locale
import urllib
import json


class SysInfo(object):

    def __init__(self):
        """
        Classe permettant de recuperer divers informations Systeme tels que
        les informations sur le materiel (les disques, processeurs, ram, ...)
        ou encore les informations systeme et Python

        """
        # -- Redefinit le locale pour les dates
        locale.setlocale(locale.LC_TIME, "")

    def getAll(self):
        """
        Retourne toutes les Infos disponibles
        """
        info = {}
        info["DATE"] = self.get_current_timestamp()
        info["DATE_FMT"] = self.get_current_formatted()
        # SYSTEM
        info["SYSTEM"] = self.getSystem()
        # SYSTEM
        info["PYTHON"] = self.getPython()
        # BOOTIME
        info["BOOTIME"] = self.getBootTime()
        # CPU
        info["CPU"] = self.getCpu()

        # MEMORY (VIRTUELLE)
        info["MEMORY_VIRT"] = self.getMemoryVirt()
        # MEMORY (SWAP)
        info["MEMORY_SWAP"] = self.getMemorySwap()

        # DISQUE
        info["DISK"] = self.get_disk_info_partition()

        # NETWORK
        info["NETWORK"] = self.getNetwork()

        """
        info["platform"] = self.get_plateform()
        info["platform-release"] = self.get_plateform_release()
        info["platform-version"] = self.get_plateform_version()
        info["today"] = self.get_today()
        info["architecture"] = self.get_archi()
        info["hostname"] = self.get_hostname()
        info["ip-address"] = self.get_ip()
        info["mac-address"] = self.get_mac_address()
        info["processor"] = self.get_processor()
        info["cpu_logical"] = self.get_cpu_logical()
        info["cpu_physical"] = self.get_cpu_physical()
        info["cpu_freq"] = self.get_cpu_freq()
        info["ram"] = self.get_ram_metrics()
        info["user"] = self.get_logon()
        """
        return info

    def getSystem(self):
        """
        Retourne un dict des infos BOOTTIME
        """
        return {
            "NAME": self.get_name_system(),
            "NODE": self.get_node_system(),
            "RELEASE": self.get_release_system(),
            "VERSION": self.get_version_system(),
            "MACHINE": self.get_machine_system(),
            "PROCESSOR": self.get_processor_system(),
        }

    def getPython(self):
        """
        Retourne un dict des infos de BOOTTIME
        """
        return {
            "VERSION": self.get_python_version(),
            "MAJEUR": self.get_python_version_majeur(),
            "MINEUR": self.get_python_version_mineur(),
            "MICRO": self.get_python_version_micro(),
            "RELEASE": self.get_python_release_level(),
        }

    def getBootTime(self):
        """
        Retourne un dict sur les infos BOOTTIME
        """
        return {
            "TIMESTAMP": self.get_bootime_timestamp(),
            "FORMATED": self.get_bootime_formatted(),
            "DELAI": self.get_bootime_delay()
        }

    def getCpu(self):
        """
        Retourne un dict sur les infos CPU
        """
        return {
            "PHYSICAL": self.get_cpu_nb_physical(),
            "LOGICAL": self.get_cpu_nb_logical(),
            "MAX_FREQ": self.get_cpu_use_max(),
            "MIN_FREQ": self.get_cpu_use_min(),
            "CUR_FREQ": self.get_cpu_use_current(),
            "CUR_FREQ_PRECENT": self.get_cpu_use_percent(),
            "USAGE_BY_CORE": self.get_cpu_use_per_core()
        }

    def getMemoryVirt(self):
        """
        Retourne un dict sur les infos MEMORY (Virtuelle)
        """
        return {
            "TOTAL": self.get_memory_virt_total(),
            "AVAILABLE": self.get_memory_virt_available(),
            "USED": self.get_memory_virt_used(),
            "PERCENT": self.get_memory_virt_percent_used(),
        }

    def getMemorySwap(self):
        """
        Retourne un dict sur les infos MEMORY (SWAP)
        """
        return {
            "TOTAL": self.get_memory_swap_total(),
            "AVAILABLE": self.get_memory_swap_available(),
            "USED": self.get_memory_swap_used(),
            "PERCENT": self.get_memory_swap_percent_used(),
        }

    def getNetwork(self):
        """
        Retourne un dict sur les infos RESEAU
        """
        return {
            "IP": self.get_network_ip(),
            "MAC": self.get_network_mac(),
            "INTERFACE": self.get_network_interfaces(),
            "PUBLIC": self.get_public_ip()
        }

    ########################################################################################################################################
    # PROPRIETES
    ########################################################################################################################################
    # -------------------------
    # PYTHON
    # -------------------------
    @staticmethod
    def get_python_version():
        """
        Retourne la version de python
        """
        return platform.python_version()

    @staticmethod
    def get_python_version_majeur():
        """
        Retourne la version de python (Majeur)
        """
        return sys.version_info[0]

    @staticmethod
    def get_python_version_mineur():
        """
        Retourne la version de python (Mineur)
        """
        return sys.version_info[1]

    @staticmethod
    def get_python_version_micro():
        """
        Retourne la version de python (Micro)
        """
        return sys.version_info[2]

    @staticmethod
    def get_python_release_level():
        """
        Retourne la release level de python
        """
        return sys.version_info[3]

    # -------------------------
    # TIME
    # -------------------------
    @staticmethod
    def get_current_timestamp():
        """
        Retourne le timestamp du moment
        """
        return time.time()

    @staticmethod
    def get_current_formatted():
        """
        Retourne une date formatté du moments
        """
        return datetime.datetime.now().strftime("%a %d %b %Y (S%W) %H:%M:%S")

    # -------------------------
    # SYSTEM
    # -------------------------

    @staticmethod
    def get_name_system():
        """Retourne le nom du system"""
        return platform.uname().system

    @staticmethod
    def get_node_system():
        """Retourne le node du system"""
        # return socket.gethostname()
        return platform.uname().node

    @staticmethod
    def get_release_system():
        """Retourne la release du system"""
        return platform.uname().release

    @staticmethod
    def get_version_system():
        """Retourne la version du system"""
        return platform.uname().version

    @staticmethod
    def get_machine_system():
        """Retourne le type de machine du system"""
        return platform.uname().machine

    @staticmethod
    def get_processor_system():
        """Retourne le type de processeur du system"""
        return platform.uname().processor

    # -------------------------
    # BOOTIME
    # -------------------------
    @staticmethod
    def get_bootime_timestamp():
        """Retourne le Timestamp du bootime"""
        return psutil.boot_time()

    @staticmethod
    def get_bootime_formatted():
        """Retourne la date formatté du bootime """
        return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%a %d %b %Y (S%W) %H:%M:%S")

    @staticmethod
    def get_bootime_delay():
        """Retourne le delai du bootime"""
        return time.time() - psutil.boot_time()

    # -------------------------
    # CPU
    # -------------------------
    @staticmethod
    def get_cpu_nb_logical():
        """Retourne le nombre de processeur LOGIQUE"""
        return psutil.cpu_count(logical=True)

    @staticmethod
    def get_cpu_nb_physical():
        """Retourne le nombre de processeur PHYSIQUE"""
        return psutil.cpu_count(logical=False)

    @staticmethod
    def get_cpu_use_percent():
        """Retourne l'utilisation processeur GLOBALE en %"""
        return psutil.cpu_percent()

    @staticmethod
    def get_cpu_use_max():
        """Retourne l'utilisation processeur MAX en MHZ"""
        return psutil.cpu_freq().max

    @staticmethod
    def get_cpu_use_min():
        """Retourne l'utilisation processeur MIN en MHZ"""
        return psutil.cpu_freq().min

    @staticmethod
    def get_cpu_use_current():
        """Retourne l'utilisation processeur COURANTE en MHZ"""
        return psutil.cpu_freq().current

    @staticmethod
    def get_cpu_use_per_core():
        """CPU Usage Par Coeurs"""
        ret = {}
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            core = {}
            core["PERCENT"] = percentage
            ret[i] = core
        return ret

    # -------------------------
    # MEMORY INFO
    # -------------------------
    @staticmethod
    def get_memory_virt_total():
        """Retourne le nombre de memoire VIRTUELLE totale"""
        return psutil.virtual_memory().total

    @staticmethod
    def get_memory_virt_available():
        """Retourne le nombre de memoire DISPONIBLE totale"""
        return psutil.virtual_memory().available

    @staticmethod
    def get_memory_virt_used():
        """Retourne le nombre de memoire UTILISE totale"""
        return psutil.virtual_memory().used

    @staticmethod
    def get_memory_virt_percent_used():
        """Retourne le nombre de memoire UTILISE totale"""
        return psutil.virtual_memory().percent

    # --------------------------------------------------
    @staticmethod
    def get_memory_swap_total():
        """Retourne le nombre de memoire SWAP totale"""
        return psutil.swap_memory().total

    @staticmethod
    def get_memory_swap_available():
        """Retourne le nombre de memoire SWAP totale"""
        return psutil.swap_memory().free

    @staticmethod
    def get_memory_swap_used():
        """Retourne le nombre de memoire SWAP totale"""
        return psutil.swap_memory().used

    @staticmethod
    def get_memory_swap_percent_used():
        """Retourne le nombre de memoire SWAP totale"""
        return psutil.swap_memory().percent

    # -------------------------
    # DISQUE
    # -------------------------
    @staticmethod
    def get_disk_info_partition():
        """Retourne les infos sur les partitions"""
        ret = {}
        cur = 0
        for partition in psutil.disk_partitions():
            disk = {
                "DEVICE": partition.device,
                "MOUNTPOINT": partition.mountpoint,
                "FILESYSTEM": partition.fstype,
            }
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # Interception en raison du disque qui
                # n'est pas prêt
                continue
            disk["TOTAL"] = partition_usage.total
            disk["USED"] = partition_usage.used
            disk["FREE"] = partition_usage.free
            disk["PERCENT"] = partition_usage.percent
            ret[cur] = disk
            cur += 1
        return ret

    # -------------------------
    # NETWORK
    # -------------------------
    @staticmethod
    def get_network_ip():
        """Retourne l'adresse IP"""
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def get_network_mac():
        """Retourne l'adresse MAC"""
        return ":".join(re.findall("..", "%012x" % uuid.getnode()))

    @staticmethod
    def get_public_ip():
        """Retourne l'adresse IP (Public)"""
        # from urllib.request import urlopen
        try:
            data = json.loads(urllib.request.urlopen("https://api.ipify.org/?format=json").read())
            return data["ip"]
        except urllib.error.HTTPError:
            return 'ERREUR'

    @staticmethod
    def get_network_interfaces():
        """Retourne les interfaces reseau"""
        ret = {}
        cur = 0
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':

                    interface = {}
                    interface["NAME"] = interface_name
                    interface["IP"] = address.address
                    interface["NETMASK"] = address.netmask
                    interface["BROADCAST_IP"] = address.broadcast

                    ret[cur] = interface
                    cur += 1
        return ret
