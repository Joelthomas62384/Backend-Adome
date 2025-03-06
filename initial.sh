#!/bin/sh

# Get the running user pod name dynamically
USER_POD=$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep "^user-")
TENANT_POD=$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep "^tenant-")

echo "User pod found: $USER_POD"
echo "Tenant pod found: $TENANT_POD"

# Define superuser credentials
SUPERUSER_EMAIL="admin@admin.com"
SUPERUSER_USERNAME="admin"
SUPERUSER_FULLNAME="admin"
SUPERUSER_PASSWORD="admin"

echo "Creating superuser in the user pod..."

# Execute commands inside the user pod
kubectl exec -it "$USER_POD" -- sh -c "
python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    user = User.objects.create_superuser(
        email='$SUPERUSER_EMAIL',
        username='$SUPERUSER_USERNAME',
        full_name='$SUPERUSER_FULLNAME',
        password='$SUPERUSER_PASSWORD'
    )
    print(f'Superuser {user.username} created successfully.')
else:
    print('Superuser already exists.')
EOF
"

echo "Superuser creation completed."

# Now execute create_public inside the tenant pod
echo "Running create_public in the tenant pod..."
kubectl exec -it "$TENANT_POD" -- sh -c "python manage.py create_public"

echo "Tenant creation completed."
