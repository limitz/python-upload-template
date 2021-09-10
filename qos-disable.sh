#!/bin/bash

TC=/sbin/tc
IFACE=eth0

$TC qdisc del dev $IFACE root
