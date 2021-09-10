#!/bin/bash

TC=/sbin/tc
IFACE=eth0
LIMIT=1000mbit
START=5mbit
BWCAP=20mbit
LOCAL=100mbit

CIDR_LOCAL=11.0.2.0/24
CIDR_UPSTR=0.0.0.0/0

#$TC qdisc del dev $IFACE root

$TC qdisc add dev $IFACE root handle 1:0 htb default 30
$TC class add dev $IFACE parent 1:0 classid 1:1 htb rate $LIMIT

$TC class add dev $IFACE parent 1:1 classid 1:10 htb rate $START ceil $LOCAL
$TC class add dev $IFACE parent 1:1 classid 1:30 htb rate $START ceil $BWCAP

$TC filter add dev $IFACE protocol ip parent 1:0 prio 1 u32 match ip dst $CIDR_LOCAL flowid 1:10
$TC filter add dev $IFACE protocol ip parent 1:0 prio 2 u32 match ip dst $CIDR_UPSTR flowid 1:30

echo "QoS should be enabled"
