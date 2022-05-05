#!/bin/bash

source backend/venv/bin/activate
python backend/app.py > /dev/null &
cd frontend || exit 1
npm run dev > /dev/null 2> /dev/null &
cd ..
