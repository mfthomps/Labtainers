az vm delete --yes --ids $(az vm list -g labtainerResources --query "[].id" -o tsv)
