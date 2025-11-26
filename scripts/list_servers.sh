#!/bin/bash

# Define the ports we expect the app to run on
PORTS="8000 8001 8002 8003 8004 8005"

echo "Checking for LeaderAI servers..."

FOUND=0

for PORT in $PORTS; do
    # Find PID using lsof (more reliable for ports)
    # We look for processes listening on TCP ports
    PID=$(lsof -ti tcp:$PORT 2>/dev/null)
    
    if [ ! -z "$PID" ]; then
        # Verify if it's a python/uvicorn process to avoid killing unrelated things
        CMD=$(ps -o command -p $PID | tail -n 1)
        if [[ "$CMD" == *"uvicorn"* ]] || [[ "$CMD" == *"python"* ]]; then
            echo "Found server on port $PORT (PID: $PID)"
            echo "  Command: $CMD"
            FOUND=1
        fi
    fi
done

if [ $FOUND -eq 0 ]; then
    echo "No running LeaderAI servers found on ports $PORTS."
    exit 0
fi
