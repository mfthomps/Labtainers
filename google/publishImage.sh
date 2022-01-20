gcloud compute images add-iam-policy-binding labtainervm \
    --member='allAuthenticatedUsers' \
    --role='roles/compute.imageUser'
