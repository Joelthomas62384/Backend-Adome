import logging
import json
from app.models import UserCache as Users, Tenants, TenantUsers

logger = logging.getLogger(__name__)

def user_callback(ch, event_type, data, method):
    try:
        if event_type == 'created':
            Users.objects.create(
                username=data['username'],
                id=data['id'],
                profile_pic=data.get('profile_pic', ''),
                full_name=data['full_name'],
                is_superuser=data['is_superuser']
            )
            logger.info(f"Created user: {data}")

        elif event_type == 'updated':
            user = Users.objects.get(id=data['id'])
            for key, value in data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            user.save()
            logger.info(f"Updated user with id: {data['id']}")

        elif event_type == 'deleted':
            Users.objects.filter(id=data['id']).delete()
            logger.info(f"Deleted user with id: {data['id']}")

        else:
            logger.warning(f"Unknown user event type: {event_type}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Users.DoesNotExist:
        logger.error(f"User with id {data.get('id', 'UNKNOWN')} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        ch.basic_ack(delivery_tag=method.delivery_tag) 

    except Exception as e:
        print(e)
        logger.error(f"Error processing user event: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)











def tenant_callback(ch, event_type, data, method):
    try:
        if event_type == 'created':
            tenant = Tenants.objects.create(
                name=data['name'],
                subscription_plan=data['subscription_plan'],
                subdomain=data['subdomain'],
                id=data['id']
            )
            try:
                admin = Users.objects.get(id=data['admin'])
                TenantUsers.objects.create(tenant=tenant, user=admin, is_admin=True)
            except Users.DoesNotExist:
                logger.warning(f"Admin user with id {data['admin']} not found for tenant {data['id']}")

            logger.info(f"Created tenant: {data}")

        elif event_type == 'updated':
            tenant = Tenants.objects.get(id=data['id'])
            for key, value in data.items():
                if hasattr(tenant, key) and value is not None:
                    setattr(tenant, key, value)
            tenant.save()
            logger.info(f"Updated tenant with id: {data['id']}")

        elif event_type == 'deleted':
            Tenants.objects.filter(id=data['id']).delete()
            logger.info(f"Deleted tenant with id: {data['id']}")

        else:
            logger.warning(f"Unknown tenant event type: {event_type}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Tenants.DoesNotExist:
        logger.error(f"Tenant with id {data.get('id', 'UNKNOWN')} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Error processing tenant event: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)













def tenantuser_callback(ch, event_type, data, method):
    try:
        if event_type == 'created':
            tenant = Tenants.objects.get(id=data['tenant'])
            user = Users.objects.get(id=data['user'])
            TenantUsers.objects.create(tenant=tenant, user=user, is_admin=data.get('is_admin', False))
            logger.info(f"Created tenant-user association: {data}")

        elif event_type == 'updated':
            tenant_user = TenantUsers.objects.get(id=data['id'])
            for key, value in data.items():
                if hasattr(tenant_user, key) and value is not None and key not in ('tenant', 'user'):
                    setattr(tenant_user, key, value)
            tenant_user.save()
            logger.info(f"Updated tenant-user with id: {data['id']}")

        elif event_type == 'deleted':
            TenantUsers.objects.filter(id=data['id']).delete()
            logger.info(f"Deleted tenant-user with id: {data['id']}")

        else:
            logger.warning(f"Unknown tenant-user event type: {event_type}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Tenants.DoesNotExist:
        logger.error(f"Tenant with id {data.get('tenant', 'UNKNOWN')} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Users.DoesNotExist:
        logger.error(f"User with id {data.get('user', 'UNKNOWN')} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except TenantUsers.DoesNotExist:
        logger.error(f"TenantUser with id {data.get('id', 'UNKNOWN')} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        logger.error("Invalid JSON received")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Error processing tenant-user event: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
