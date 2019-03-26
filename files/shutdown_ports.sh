#!/bin/bash

ports=$(/bin/ip link | grep swp | wc -l)
for i in $( seq 1 $ports ); do
   ip link set swp$i down
done
