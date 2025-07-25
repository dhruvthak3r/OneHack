#!/bin/sh

# Start the email consumer in the background
#python notifications/receivers/receive_emails.py &

# Start the hackathon consumer in the background
#python notifications/receivers/receive_hackathons.py &

# Start the FastAPI server (in the foreground)
uvicorn app.main:app --host 0.0.0.0 --port 8080
