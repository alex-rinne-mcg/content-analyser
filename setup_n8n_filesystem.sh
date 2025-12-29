#!/bin/bash

# N8N Filesystem Mode Setup Script
# This script helps configure N8N_DEFAULT_BINARY_DATA_MODE=filesystem

set -e

echo "🔍 N8N Filesystem Mode Setup"
echo "============================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if variable is set
check_env_var() {
    if [ -n "$1" ]; then
        echo -e "${GREEN}✓${NC} $2 is set: $1"
        return 0
    else
        echo -e "${RED}✗${NC} $2 is not set"
        return 1
    fi
}

# Check current N8N installation
echo "1. Checking N8N installation method..."
echo ""

# Check for Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    if docker ps | grep -q n8n; then
        echo -e "${YELLOW}→${NC} N8N appears to be running in Docker"
        DOCKER_N8N=$(docker ps | grep n8n | awk '{print $1}')
        echo "  Container ID: $DOCKER_N8N"
        
        # Check current env var
        CURRENT_MODE=$(docker inspect $DOCKER_N8N 2>/dev/null | grep -i "N8N_DEFAULT_BINARY_DATA_MODE" | head -1 || echo "")
        if [ -n "$CURRENT_MODE" ]; then
            echo -e "  ${GREEN}Current setting:${NC} $CURRENT_MODE"
        else
            echo -e "  ${RED}N8N_DEFAULT_BINARY_DATA_MODE is not set${NC}"
        fi
        
        INSTALL_METHOD="docker"
    fi
fi

# Check for systemd
if systemctl list-units --type=service 2>/dev/null | grep -q n8n; then
    echo -e "${GREEN}✓${NC} N8N systemd service found"
    INSTALL_METHOD="systemd"
    
    # Check current env var
    if systemctl show n8n 2>/dev/null | grep -q "N8N_DEFAULT_BINARY_DATA_MODE"; then
        CURRENT_MODE=$(systemctl show n8n | grep "N8N_DEFAULT_BINARY_DATA_MODE")
        echo -e "  ${GREEN}Current setting:${NC} $CURRENT_MODE"
    else
        echo -e "  ${RED}N8N_DEFAULT_BINARY_DATA_MODE is not set${NC}"
    fi
fi

# Check for .env file
if [ -f ~/.n8n/.env ]; then
    echo -e "${GREEN}✓${NC} Found ~/.n8n/.env"
    INSTALL_METHOD="env_file"
    
    if grep -q "N8N_DEFAULT_BINARY_DATA_MODE" ~/.n8n/.env; then
        CURRENT_MODE=$(grep "N8N_DEFAULT_BINARY_DATA_MODE" ~/.n8n/.env)
        echo -e "  ${GREEN}Current setting:${NC} $CURRENT_MODE"
    else
        echo -e "  ${RED}N8N_DEFAULT_BINARY_DATA_MODE is not set${NC}"
    fi
fi

# Check for docker-compose.yml
if [ -f docker-compose.yml ]; then
    echo -e "${GREEN}✓${NC} Found docker-compose.yml in current directory"
    INSTALL_METHOD="docker_compose"
    
    if grep -q "N8N_DEFAULT_BINARY_DATA_MODE" docker-compose.yml; then
        CURRENT_MODE=$(grep "N8N_DEFAULT_BINARY_DATA_MODE" docker-compose.yml)
        echo -e "  ${GREEN}Current setting:${NC} $CURRENT_MODE"
    else
        echo -e "  ${RED}N8N_DEFAULT_BINARY_DATA_MODE is not set${NC}"
    fi
fi

echo ""
echo "2. Configuration options:"
echo ""

if [ -z "$INSTALL_METHOD" ]; then
    echo -e "${YELLOW}⚠${NC} Could not detect N8N installation method automatically"
    echo ""
    echo "Please choose your installation method:"
    echo "  1) Docker Compose"
    echo "  2) Docker Run"
    echo "  3) Systemd Service"
    echo "  4) .env file (~/.n8n/.env)"
    echo "  5) N8N Cloud (manual configuration)"
    echo ""
    read -p "Enter choice (1-5): " choice
    
    case $choice in
        1) INSTALL_METHOD="docker_compose" ;;
        2) INSTALL_METHOD="docker_run" ;;
        3) INSTALL_METHOD="systemd" ;;
        4) INSTALL_METHOD="env_file" ;;
        5) INSTALL_METHOD="cloud" ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac
fi

echo ""
echo "3. Setting up filesystem mode..."
echo ""

case $INSTALL_METHOD in
    docker_compose)
        if [ -f docker-compose.yml ]; then
            echo "Updating docker-compose.yml..."
            
            # Check if environment section exists
            if grep -q "environment:" docker-compose.yml; then
                # Add to existing environment section
                if ! grep -q "N8N_DEFAULT_BINARY_DATA_MODE" docker-compose.yml; then
                    # Add after environment: line
                    sed -i.bak '/environment:/a\      - N8N_DEFAULT_BINARY_DATA_MODE=filesystem' docker-compose.yml
                    echo -e "${GREEN}✓${NC} Added N8N_DEFAULT_BINARY_DATA_MODE=filesystem to docker-compose.yml"
                else
                    echo -e "${YELLOW}⚠${NC} N8N_DEFAULT_BINARY_DATA_MODE already exists in docker-compose.yml"
                fi
            else
                # Add environment section
                echo "    environment:" >> docker-compose.yml
                echo "      - N8N_DEFAULT_BINARY_DATA_MODE=filesystem" >> docker-compose.yml
                echo -e "${GREEN}✓${NC} Added environment section to docker-compose.yml"
            fi
            
            echo ""
            echo "To apply changes, run:"
            echo -e "${GREEN}  docker-compose down && docker-compose up -d${NC}"
        else
            echo -e "${RED}✗${NC} docker-compose.yml not found in current directory"
        fi
        ;;
        
    docker_run)
        echo "For Docker Run, add this flag to your docker run command:"
        echo -e "${GREEN}  -e N8N_DEFAULT_BINARY_DATA_MODE=filesystem${NC}"
        echo ""
        echo "Example:"
        echo "  docker run -it --rm \\"
        echo "    --name n8n \\"
        echo "    -p 5678:5678 \\"
        echo "    -e N8N_DEFAULT_BINARY_DATA_MODE=filesystem \\"
        echo "    -v ~/.n8n:/home/node/.n8n \\"
        echo "    n8nio/n8n"
        ;;
        
    systemd)
        SERVICE_FILE="/etc/systemd/system/n8n.service"
        USER_SERVICE_FILE="$HOME/.config/systemd/user/n8n.service"
        
        if [ -f "$SERVICE_FILE" ]; then
            SERVICE_PATH="$SERVICE_FILE"
            SUDO_CMD="sudo"
        elif [ -f "$USER_SERVICE_FILE" ]; then
            SERVICE_PATH="$USER_SERVICE_FILE"
            SUDO_CMD=""
        else
            echo -e "${RED}✗${NC} N8N service file not found"
            echo "Expected locations:"
            echo "  - $SERVICE_FILE"
            echo "  - $USER_SERVICE_FILE"
            exit 1
        fi
        
        echo "Updating service file: $SERVICE_PATH"
        
        if grep -q "N8N_DEFAULT_BINARY_DATA_MODE" "$SERVICE_PATH"; then
            echo -e "${YELLOW}⚠${NC} N8N_DEFAULT_BINARY_DATA_MODE already exists"
        else
            # Add Environment line in [Service] section
            $SUDO_CMD sed -i.bak '/\[Service\]/a Environment="N8N_DEFAULT_BINARY_DATA_MODE=filesystem"' "$SERVICE_PATH"
            echo -e "${GREEN}✓${NC} Added N8N_DEFAULT_BINARY_DATA_MODE=filesystem to service file"
        fi
        
        echo ""
        echo "To apply changes, run:"
        if [ -n "$SUDO_CMD" ]; then
            echo -e "${GREEN}  sudo systemctl daemon-reload${NC}"
            echo -e "${GREEN}  sudo systemctl restart n8n${NC}"
        else
            echo -e "${GREEN}  systemctl --user daemon-reload${NC}"
            echo -e "${GREEN}  systemctl --user restart n8n${NC}"
        fi
        ;;
        
    env_file)
        ENV_FILE="$HOME/.n8n/.env"
        
        # Create directory if it doesn't exist
        mkdir -p "$HOME/.n8n"
        
        if [ -f "$ENV_FILE" ]; then
            if grep -q "N8N_DEFAULT_BINARY_DATA_MODE" "$ENV_FILE"; then
                # Update existing
                sed -i.bak 's/^N8N_DEFAULT_BINARY_DATA_MODE=.*/N8N_DEFAULT_BINARY_DATA_MODE=filesystem/' "$ENV_FILE"
                echo -e "${GREEN}✓${NC} Updated N8N_DEFAULT_BINARY_DATA_MODE in $ENV_FILE"
            else
                # Add new
                echo "N8N_DEFAULT_BINARY_DATA_MODE=filesystem" >> "$ENV_FILE"
                echo -e "${GREEN}✓${NC} Added N8N_DEFAULT_BINARY_DATA_MODE=filesystem to $ENV_FILE"
            fi
        else
            # Create new file
            echo "N8N_DEFAULT_BINARY_DATA_MODE=filesystem" > "$ENV_FILE"
            echo -e "${GREEN}✓${NC} Created $ENV_FILE with N8N_DEFAULT_BINARY_DATA_MODE=filesystem"
        fi
        
        echo ""
        echo "To apply changes, restart N8N:"
        echo -e "${GREEN}  n8n restart${NC}"
        echo "  or stop and start N8N manually"
        ;;
        
    cloud)
        echo "For N8N Cloud:"
        echo "1. Go to your N8N Cloud dashboard"
        echo "2. Navigate to Settings → Environment Variables"
        echo "3. Add new variable:"
        echo "   Name: N8N_DEFAULT_BINARY_DATA_MODE"
        echo "   Value: filesystem"
        echo "4. Save and restart your instance"
        ;;
esac

echo ""
echo "4. Verification:"
echo ""
echo "After restarting N8N, verify the setting:"
echo ""
echo "  - Check N8N UI → Settings → Environment Variables"
echo "  - Or check logs for confirmation"
echo ""
echo -e "${GREEN}✓${NC} Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Restart N8N (if not done automatically)"
echo "  2. Test the workflow with a video post"
echo "  3. Check that videos are processed without memory errors"

