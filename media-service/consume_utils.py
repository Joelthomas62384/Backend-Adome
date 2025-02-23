import logging
import json
from django.db.utils import IntegrityError
from app.models import UserCache as Users

logger = logging.getLogger(__name__)

def user_callback(ch, event_type, data, method):
    try:
        user_id = data.get("id")  
        if event_type == "created":
            Users.objects.create(username=data["username"] , id=data['id'])
            logger.info(f"Created user with data: {data}")

        elif event_type == "updated":
            if not user_id:
                logger.error("Missing user ID for update event")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                return

            user = Users.objects.get(id=user_id)

            for key, value in data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            user.save()

            logger.info(f"Updated user with ID: {user_id}")

        elif event_type == "deleted":
            if not user_id:
                logger.error("Missing user ID for delete event")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                return

            Users.objects.get(id=user_id).delete()
            logger.info(f"Deleted user with ID: {user_id}")

        else:
            logger.warning(f"Unknown event type: {event_type}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Users.DoesNotExist:
        logger.error(f"User with ID {user_id} not found")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except IntegrityError as e:
        logger.error(f"Database Integrity Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as e:
        logger.error(f"Processing error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) 
