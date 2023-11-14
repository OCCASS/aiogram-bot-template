#!/bin/bash

if [[ "$1" -eq "" ]]; then
    echo "Usage: $0 \"message\""
    exit 1
fi

alembic revision --autogenerate -m $1

