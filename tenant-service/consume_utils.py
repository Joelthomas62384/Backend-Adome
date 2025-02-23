import logging
from app.models import UserCache as Users
import json

logger = logging.getLogger(__name__)





def user_callback(ch, event_type , data , method):
    try:
        

        if event_type == 'created' :
            Users.objects.create(username = data['username'] , id=data['id'])


            logger.info(f"Created user with data: {data}")


        elif event_type == 'updated':
            user = Users.objects.get(id=data['id'])


            for key, value in data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            user.save()


            logger.info(f"Updated Users with id: {data['id']}")


        elif event_type == 'deleted':

            Users.objects.get(id=data['id']).delete()

            logger.info(f"Deleted Users with id: {data['id']}")


        else:

            logger.warning(f"Unknown event type: {event_type}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)


    except json.JSONDecodeError as e:

        
        logger.error(f"Invalid JSON: {e}")

        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Users.DoesNotExist:

        logger.error(f"Users with id {data.get('id')} not found")

        ch.basic_ack(delivery_tag=method.delivery_tag)  

    except Exception as e:

        logger.error(f"Processing error: {e}")


        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)