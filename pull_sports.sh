#!/bin/bash
#
# file: pull_sports.sh
#
# description: downloads medal summaries for all olympic sports
#
# usage: ./pull_sports.sh
#
# requirements: wget
#
# author: jake hofman (gmail: jhofman)
#

wget -mkr -l 2 -np -w 3 --random-wait http://www.sports-reference.com/olympics/sports/
