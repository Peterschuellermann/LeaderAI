#!/bin/bash

# Define the ports we expect the app to run on
PORTS="8000 8001 8002 8003 8004 8005"

echo "Stopping LeaderAI servers..."

STOPPED=0

for PORT in $PORTS; do
    # Find PID using lsof
    PIDS=$(lsof -ti tcp:$PORT 2>/dev/null)
    
    for PID in $PIDS; do
        if [ ! -z "$PID" ]; then
            CMD=$(ps -o command -p $PID | tail -n 1)
            # Safety check: only kill uvicorn/python processes
            if [[ "$CMD" == *"uvicorn"* ]] || [[ "$CMD" == *"python"* ]]; then
                echo "Killing process on port $PORT (PID: $PID)..."
                kill -TERM "$PID" 2>/dev/null
                
                # Wait a moment and check if it's still there
                sleep 1
                if ps -p $PID > /dev/null 2>&1; then
                    echo "  Process $PID did not stop, force killing..."
                    kill -KILL "$PID" 2>/dev/null
                fi
                STOPPED=1
            fi
        fi
    done
done

if [ $STOPPED -eq 0 ]; then
    echo "No LeaderAI servers found to stop."
else
    echo "All detected servers stopped."
fi
