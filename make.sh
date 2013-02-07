#!/bin/sh
( sed -n 1p initctl; cat UpstartConfigParser.py; echo; sed -n 2,8p initctl; sed -n '10,$p' initctl ) > sbin_initctl
