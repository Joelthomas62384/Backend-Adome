#!/bin/sh

# Get the running tenant pod name dynamically
TENANT_POD=$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep "^user-")

# Check if a tenant pod was found
if [ -z "$TENANT_POD" ]; then
    echo "Error: No running tenant pod found."
    exit 1
fi

echo "Tenant pod found: $TENANT_POD"

# Execute the create_dummy_users command inside the tenant pod
echo "Running create_dummy_users in the tenant pod..."
kubectl exec -it "$TENANT_POD" -- sh -c "python manage.py create_dummy_users"

echo "Dummy user creation completed."
