#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This package implement netbios and LLMNR query tool in python and HostnameResolver command line tool. """

###################
#    This package implement netbios and LLMNR query tool in python and HostnameResolver command line tool.
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

from ipaddress import ip_address
from argparse import ArgumentParser
from .NetbiosResolver import ResolveNetbios
from socket import gethostbyaddr, gaierror, herror, gethostbyname_ex


def parse():
    parser = ArgumentParser()
    parser.add_argument(
        "IP_HOSTNAMES",
        help="IP or hostnames to resolve (example: 192.168.1.2,Windows10,HOME-PC).",
    )
    return parser.parse_args()


def is_ip(ip_hostname):
    try:
        ip_address(ip_hostname)
    except ValueError:
        return False
    else:
        return True


def socket_resolver(ip_hostname):
    try:
        hostname, alias, ip = gethostbyaddr(ip_hostname)
    except gaierror:
        pass
    except herror:
        pass
    else:
        return hostname, alias, ip

    try:
        hostname, alias, ip = gethostbyname_ex(ip_hostname)
    except gaierror:
        return
    except herror:
        return
    else:
        return hostname, alias, ip


def resolve_local_ip(ip):
    netbios = ResolveNetbios(ip)
    hostname = netbios.resolve_NBTNS()
    if not hostname:
        hostname = netbios.resolve_LLMNR()
    return hostname or ""


def main():
    parser = parse()
    ip_hostnames = parser.IP_HOSTNAMES.split(",")

    for ip_hostname in ip_hostnames:
        print(f"\nResolve {ip_hostname}...")
        hostname, alias, ip = None, None, None

        resolve = socket_resolver(ip_hostname)

        if (not resolve or resolve[0] == resolve[2][0]) and is_ip(ip_hostname):
            hostname, ip, alias = resolve_local_ip(ip_hostname), ip_hostname, None
        elif resolve:
            hostname, alias, ip = resolve
            alias = ", ".join(alias)
            ip = ", ".join(ip)
        else:
            print(f"\t - Hostname: {ip_hostname} can't be result.")

        if hostname:
            print(f"\t - Hostname for {ip_hostname}: {hostname}")
        if ip:
            print(f"\t - IP for {ip_hostname}: {ip}")
        if alias:
            print(f"\t - Alias for {ip_hostname}: {alias}")


def resolve_all(results, ip_hostname):
    resolve = socket_resolver(ip_hostname)

    hostname, alias, ip = "", "", ""

    if (not resolve or resolve[0] == resolve[2][0]) and is_ip(ip_hostname):
        hostname, ip = resolve_local_ip(ip_hostname), ip_hostname
    elif resolve:
        hostname, alias, ip = resolve
        alias = ", ".join(alias)
        ip = ", ".join(ip)

    results[ip_hostname] = (hostname, alias, ip)


def main_thread():
    from threading import Thread, enumerate, current_thread

    parser = parse()
    ip_hostnames = parser.IP_HOSTNAMES.split(",")
    results = {}

    for ip_hostname in ip_hostnames:
        Thread(
            target=resolve_all,
            args=(
                results,
                ip_hostname,
            ),
        ).start()

    current = current_thread()
    for thread in enumerate():
        if current is not thread:
            thread.join()

    for ip_hostname, results_ in results.items():
        print(
            f"\nQuery: {ip_hostname}\n\t - Hostname: {results_[0]}\n\t - Alias: {results_[1]}\n\t - IP: {results_[2]}"
        )


if __name__ == "__main__":
    main_thread()
