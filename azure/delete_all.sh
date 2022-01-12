az vm delete --force --ids $(az vm list -g labtainerResources --query "[].id" -o tsv)
