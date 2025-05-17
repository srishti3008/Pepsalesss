from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app import models, tasks
from app.models import Notification, NotificationIn, NotificationOut

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Notification Service", version="1.0.0")


@app.post("/notifications", response_model=NotificationOut, status_code=status.HTTP_202_ACCEPTED)
def send_notification(payload: NotificationIn, db: Session = Depends(get_db)):
    notif = Notification(**payload.dict())
    db.add(notif)
    db.commit()
    db.refresh(notif)
    tasks.deliver.delay(str(notif.id))
    return notif


@app.get("/users/{user_id}/notifications", response_model=list[NotificationOut])
def list_notifications(user_id: str, db: Session = Depends(get_db)):
    rows = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return rows