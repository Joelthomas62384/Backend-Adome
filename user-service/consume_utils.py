from app.models import TenantUsers, Tenants, User
import logging

logger = logging.getLogger(__name__)

def tenant_callback(ch, event_type, data, method):
    try:
        if not isinstance(data, dict):
            logger.error(f"Invalid data type: {type(data)} - {data}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        if event_type == 'created':
            tenant = Tenants.objects.create(name=data['name'], subdomain=data['subdomain'], id=data['id'])
            user = User.objects.get(id=data['admin'])
            TenantUsers.objects.create(tenant=tenant, user=user, is_admin=True)
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
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                return

        elif event_type == 'deleted':
            try:
                Tenants.objects.get(id=data['id']).delete()
                logger.info(f"Deleted Tenant with id: {data['id']}")
            except Tenants.DoesNotExist:
                logger.warning(f"Tenant with id {data['id']} not found, nothing to delete.")

        else:
            logger.warning(f"Unknown event type: {event_type}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
