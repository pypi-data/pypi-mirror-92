#!/bin/bash

pod2man -r "pg_activity 2.0.0" -d `date +%Y-%m-%d` -c "Command line tool for PostgreSQL server activity monitoring." pg_activity.pod > pg_activity.1;
