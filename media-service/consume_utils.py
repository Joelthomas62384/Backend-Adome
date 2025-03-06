import logging
import json
from django.db.utils import IntegrityError
from app.models import UserCache as Users , Tenants

logger = logging.getLogger(__name__)

def user_callback(ch, event_type, data, method):
    try:
        user_id = data.get("id")
        if not user_id:
            logger.error("Missing user ID in event data")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return

        if event_type == "created":
            user, created = Users.objects.get_or_create(id=user_id, defaults={
                "username": data["username"]
            })
            if created:
                logger.info(f"Created user: {data}")
            else:
                logger.warning(f"User with ID {user_id} already exists")

        elif event_type == "updated":
            updated_fields = {k: v for k, v in data.items() if v is not None and hasattr(Users, k)}
            if updated_fields:
                Users.objects.filter(id=user_id).update(**updated_fields)
                logger.info(f"Updated user with ID: {user_id}")
            else:
                logger.warning(f"No valid fields to update for user ID: {user_id}")

        elif event_type == "deleted":
            deleted_count, _ = Users.objects.filter(id=user_id).delete()
            if deleted_count:
                logger.info(f"Deleted user with ID: {user_id}")
            else:
                logger.warning(f"User with ID {user_id} not found for deletion")

        else:
            logger.warning(f"Unknown event type: {event_type}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except IntegrityError as e:
        logger.error(f"Database Integrity Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)



def tenant_callback(ch, event_type, data, method):
    try:
        if not isinstance(data, dict):
            logger.error(f"Invalid data type: {type(data)} - {data}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return

        if event_type == 'created':
            tenant = Tenants.objects.create(name=data['name'], subdomain=data['subdomain'], id=data['id'])
           
            logger.info(f"Created tenant with data: {data}")

        elif event_type == 'updated':
            try:
                tenant = Tenants.objects.get(id=data['id'])
                for key, value in data.items():
                    if hasattr(tenant, key) and value is not None:
                        setattr(tenant, key, value)
                tenant.save()
                logger.info(f"Updated Tenant with id: {data['id']}")
            except Tenants.DoesNotExist:
                logger.error(f"Tenant with id {data['id']} not found")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                return

        elif event_type == 'deleted':
            try:
                Tenants.objects.get(id=data['id']).delete()
                logger.info(f"Deleted Tenant with id: {data['id']}")
            except Tenants.DoesNotExist:
                logger.warning(f"Tenant with id {data['id']} not found, nothing to delete.")

        else:
            logger.warning(f"Unknown event type: {event_type}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
