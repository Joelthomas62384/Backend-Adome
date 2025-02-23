#!/bin/bash

# Loop through all pods except rootdb and rabbitmq
for pod in $(kubectl get pods -o custom-columns=":metadata.name" --no-headers | grep -vE "rootdb|rabbitmq"); do
  echo "migrating database for $pod..."
  kubectl exec -it $pod -- python manage.py migrate --no-input
done
