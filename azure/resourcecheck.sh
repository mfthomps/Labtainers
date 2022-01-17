#!/bin/bash
result=$(az group list | grep labtainerResources)
if [ -z "${result}" ]; then
    echo "Creating Labtainer resource group."
    az group create -l westus2 -n labtainerResources --output none
else
    echo "Labtainer resource group exists."
fi
