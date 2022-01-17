#!/bin/bash
result=$(az group list | grep labtainerResources)
if [ -z "${result}" ]; then
    echo "Creating Labtainer resource group."
    az group create -l westus3 -n labtainerResources --output none || exit 1
else
    echo "Labtainer resource group exists."
fi
