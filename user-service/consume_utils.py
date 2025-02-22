from app.models import TenantUsers , Tenants
import json
import logging

logger = logging.getLogger(__name__)


def tenant_callback(ch, event_type , data , method):
    try:
        
       

        if event_type == 'created' :
            Tenants.objects.create(**data)
            logger.info(f"Created tenant with data: {data}")
        elif event_type == 'updated':
            tenant = Tenants.objects.get(id=data['id'])
            for key, value in data.items():
                setattr(tenant, key, value)
            tenant.save()
            logger.info(f"Updated Tenants with id: {data['id']}")
        elif event_type == 'deleted':
            Tenants.objects.get(id=data['id']).delete()
            logger.info(f"Deleted Tenants with id: {data['id']}")
        else:
            logger.warning(f"Unknown event type: {event_type}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Tenants.DoesNotExist:
        logger.error(f"Tenants with id {data.get('id')} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)  
    except Exception as e:
        logger.error(f"Processing error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)