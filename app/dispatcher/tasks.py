import datetime as dt, logging
from sqlalchemy.orm import Session
from .broker import celery_app
from .database import SessionLocal
from .models import Notification
from .dispatchers.email import EmailDispatcher
from .dispatchers.sms import SMSDispatcher
from .dispatchers.in_app import InAppDispatcher
from .settings import settings

log = logging.getLogger(__name__)

dispatch_map = {
    "email": EmailDispatcher(),
    "sms": SMSDispatcher(),
    "in_app": InAppDispatcher(),
}


@celery_app.task(bind=True, max_retries=settings.MAX_RETRIES, acks_late=True)
def deliver(self, notif_id: str):
    db: Session = SessionLocal()
    notif: Notification = db.get(Notification, notif_id)
    try:
        dispatcher = dispatch_map[notif.channel.value]
        dispatcher.send(notif)
        notif.sent = True
        notif.sent_at = dt.datetime.utcnow()
        db.commit()
    except Exception as exc:
        db.rollback()
        log.error("Delivery failed – retrying...", exc_info=True)
        self.retry(exc=exc, countdown=settings.RETRY_BACKOFF)
    finally:
        db.close()