from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Alert
from priority_score import calculate_priority_score

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/alerts/{alert_id}/priority")
def get_alert_priority(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")

    try:
        priority_score = calculate_priority_score(
            alert.severity,
            alert.metric_value,
            alert.threshold,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {"alert_id": alert.id, "priority_score": priority_score}