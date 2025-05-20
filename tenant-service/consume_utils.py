import logging
from app.models import UserCache as Users , Tenants

logger = logging.getLogger(__name__)

def user_callback(ch, event_type, data, method):
    try:
        if not isinstance(data, dict):
            logger.error(f"Invalid data type received: {type(data)} - {data}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  
            return

        user_id = data.get('id')
        if not user_id:
            logger.error("User ID missing in event data")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  
            return

        if event_type == 'created':
            Users.objects.create(username=data['username'], id=user_id)
            logger.info(f"Created user with ID: {user_id}")

        elif event_type == 'updated':
            try:
                user = Users.objects.get(id=user_id)
                for key, value in data.items():
                    if hasattr(user, key) and value is not None:
                        setattr(user, key, value)
                user.save()
                logger.info(f"Updated user with ID: {user_id}")
            except Users.DoesNotExist:
                logger.error(f"User with ID {user_id} not found for update")
                ch.basic_ack(delivery_tag=method.delivery_tag) 
                return

        elif event_type == 'deleted':
            try:
                Users.objects.get(id=user_id).delete()
                logger.info(f"Deleted user with ID: {user_id}")
            except Users.DoesNotExist:
                logger.warning(f"User with ID {user_id} not found for deletion")
                ch.basic_ack(delivery_tag=method.delivery_tag)  
                return

        else:
            logger.warning(f"Unknown event type: {event_type}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) 
            return

        ch.basic_ack(delivery_tag=method.delivery_tag)  

    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) 



def subscription_callback(ch, event_type, data, method):
    try:
        if not isinstance(data, dict):
            logger.error(f"Invalid data type received: {type(data)} - {data}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  
            return
        tenant = Tenants.objects.filter(id=data['tenant'])
        if not tenant.exists():
            logger.error(f"Invalid data type received: {type(data)} - {data}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  
            return
        tenant = tenant.first()
        tenant.subscription_plan = data['plan']
        tenant.save()
        ch.basic_ack(delivery_tag=method.delivery_tag)  







    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) 

