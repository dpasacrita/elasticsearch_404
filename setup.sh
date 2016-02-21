#!/bin/bash
# setup.sh
# This script will install the dependencies required for the 404 script and will also create
# the necessary directories.

# Load Bash Profile
. ~/.bash_profile

# Check to make sure the script has been run as root.
if [[ $EUID -ne 0 ]]; then
        echo "The setup script must be run as root." 1>&2
        exit 10
fi

# Install Python
echo "Installing python3..."
yum install python -y
# Check if python installed successfully
if [ $? -eq 0 ]
then
    echo "Python installed."
else
    echo "Python installation failed. Check connection/yum." >&2
    exit 1
fi

# Install Development Tools
echo "Installing python3..."
yum groupinstall "Development Tools" -y
# Check if they installed successfully
if [ $? -eq 0 ]
then
    echo "Development Tools installed."
else
    echo "Installation failed. Check connection/yum." >&2
    exit 1
fi

# Install Mutt
echo "Installing mutt..."
yum install mutt -y
# Check if mutt installed successfully
if [ $? -eq 0 ]
then
    echo "Mutt installed."
else
    echo "Mutt installation failed. Check connection/yum." >&2
    exit 2
fi

# Install Python Libraries
echo "Installing Python libraries..."
echo "elasticsearch:"
pip install elasticsearch
# Check if python installed successfully
if [ $? -eq 0 ]
then
    echo "Elasticsearch library installed."
else
    echo "Installation failed. Check pip settings." >&2
    exit 3
fi
echo "xlwt:"
pip install xlwt
# Check if python installed successfully
if [ $? -eq 0 ]
then
    echo "xlwt library installed."
else
    echo "Installation failed. Check pip settings." >&2
    exit 4
fi

# Complete
echo "All dependencies installed."
exit 0

