FROM n8nio/n8n:latest

# Set environment variables for binary data handling
ENV N8N_DEFAULT_BINARY_DATA_MODE=filesystem
ENV N8N_BINARY_DATA_STORAGE_PATH=/home/node/.n8n/binaryData

# Create binary data directory
RUN mkdir -p /home/node/.n8n/binaryData && \
    chown -R node:node /home/node/.n8n

USER node

WORKDIR /home/node

# Expose N8N port
EXPOSE 5678

# Start N8N
CMD ["n8n", "start"]

