#!/bin/bash

# Generate a secure encryption key for N8N
# This is required for Railway deployment

echo "Generating N8N encryption key..."
echo ""
echo "Add this to your Railway environment variables as N8N_ENCRYPTION_KEY:"
echo ""
openssl rand -base64 32
echo ""
echo "✅ Copy the key above and add it to Railway → Variables → N8N_ENCRYPTION_KEY"

