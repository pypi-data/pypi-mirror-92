#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This package implement a hostname resolver (and reverse hostname). """

###################
#    This package implement a hostname resolver (and reverse hostname).
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

from scapy.all import (
    DNSQR,
    DNSRR,
    LLMNRQuery,
    LLMNRResponse,
    IP,
    IPv6,
    UDP,
    NBNSQueryRequest,
    Raw,
    sr1,
    send,
    AsyncSniffer,
)
from time import sleep


class ResolveNetbios:
    def __init__(self, ip, timeout=3):
        self.ip = ip
        self.nom = None
        self.timeout = timeout

    def resolve_NBTNS(self):
        response = sr1(
            IP(dst=self.ip)
            / UDP(sport=137, dport=137)
            / NBNSQueryRequest(
                FLAGS=0, QDCOUNT=1, QUESTION_NAME="*" + "\x00" * 14, QUESTION_TYPE=33
            ),
            timeout=self.timeout,
            verbose=0,
        )

        if response and response.haslayer(Raw):
            self.nom = ""
            for car in response[Raw].load:
                car = chr(car)
                if car == " " or (car == "\x00" and len(self.nom)):
                    return self.nom
                elif car in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-":
                    self.nom += car
        else:
            return None

    def resolve_LLMNR(self):
        self.no_LLMNRResponse = True
        name = ".".join(self.ip.split(".")[::-1]) + ".in-addr.arpa."

        sniffer = AsyncSniffer(
            filter="port 5355 and proto UDP",
            prn=lambda packet: self.check_LLMNR(packet, name),
        )
        sniffer.start()

        self.send_LLMNRQuery(name)
        sniffer.stop()

        if not self.no_LLMNRResponse:
            return self.nom

    def send_LLMNRQuery(self, name):
        for a in range(5):
            send(
                IP(dst="224.0.0.252")
                / UDP(dport=5355)
                / LLMNRQuery(qdcount=1, qd=DNSQR(qtype=12, qname=name)),
                verbose=0,
            )
            send(
                IPv6(dst="ff02::1:3")
                / UDP(dport=5355)
                / LLMNRQuery(qdcount=1, qd=DNSQR(qtype=12, qname=name)),
                inter=1,
                count=2,
                verbose=0,
            )
            if not self.no_LLMNRResponse:
                break

        if self.no_LLMNRResponse:
            sleep(self.timeout)

    def check_LLMNR(self, packet, name):
        if packet.haslayer(LLMNRResponse) and packet.haslayer(DNSRR):
            if packet[DNSRR].rrname == name.encode():
                self.no_LLMNRResponse = False
                self.nom = packet[DNSRR].rdata.decode()
