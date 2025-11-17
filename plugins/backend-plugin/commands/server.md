---
description: Manage backend servers - start, stop, restart, and check status
allowed-tools: Bash, Read
---

# Server Command

Start, stop, and manage backend servers across different languages and frameworks.

## Usage

`/server [action] [port]`

## Actions

- `start` - Start development server
- `stop` - Stop server
- `restart` - Restart server
- `status` - Check server status
- `logs` - Show server logs

## Implementation

!`#!/bin/bash

ACTION=${1:-status}
PORT=${2:-3000}

case $ACTION in
  start)
    echo "Starting server on port $PORT..."
    if [ -f "package.json" ]; then
      # Node.js project
      if grep -q "\"dev\"" package.json; then
        npm run dev
      else
        npm start
      fi
    elif [ -f "go.mod" ]; then
      # Go project
      go run . &
      echo "Go server started with PID $!"
    elif [ -f "manage.py" ]; then
      # Django project
      python manage.py runserver 0.0.0.0:$PORT
    elif [ -f "main.py" ] || [ -f "app.py" ]; then
      # FastAPI/Flask project
      if grep -q "fastapi" requirements.txt 2>/dev/null || grep -q "FastAPI" pyproject.toml 2>/dev/null; then
        uvicorn main:app --reload --port $PORT --host 0.0.0.0
      else
        python main.py
      fi
    else
      echo "No supported project type found in current directory"
      exit 1
    fi
    ;;
  stop)
    echo "Stopping server..."
    pkill -f "node|go run|python|uvicorn" || echo "No server processes found"
    ;;
  restart)
    $0 stop
    sleep 2
    $0 start $PORT
    ;;
  status)
    echo "Checking server status..."
    ps aux | grep -E "node|go run|python|uvicorn" | grep -v grep || echo "No server is running"
    ;;
  logs)
    echo "Showing recent logs..."
    if [ -f "logs/app.log" ]; then
      tail -f logs/app.log
    else
      echo "No log files found"
    fi
    ;;
  *)
    echo "Usage: /server [start|stop|restart|status|logs] [port]"
    exit 1
    ;;
esac
`