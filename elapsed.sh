#!/usr/bin/env bash

# Argument $1: Reference timestamp (e.g., "2026-01-01 12:00:00")
if [[ -z "$1" ]]; then
    echo '{"text": "ERR", "tooltip": "Missing timestamp argument"}'
    exit 1
fi

START=$(date -d "$1" +%s 2>/dev/null)
if [[ $? -ne 0 ]]; then
    echo '{"text": "ERR", "tooltip": "Invalid date format"}'
    exit 1
fi

NOW=$(date +%s)
DIFF=$((NOW - START))

# Arithmetic for time units
DAYS=$((DIFF / 86400))
HOURS=$(( (DIFF % 86400) / 3600 ))
MINS=$(( (DIFF % 3600) / 60 ))

# Output JSON
printf '{"text": "%dd %02dh %02dm", "tooltip": "Time elapsed since %s"}\n' \
    "$DAYS" "$HOURS" "$MINS" "$1"
