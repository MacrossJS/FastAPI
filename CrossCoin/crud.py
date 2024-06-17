from sqlalchemy.orm import Session
import models
import schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str):
    db_user = models.User(username=username, coins=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_coins(db: Session, user: models.User):
    user.coins += 1
    db.commit()
    db.refresh(user)
    return user


def get_leaderboard(db: Session):
    return db.query(models.User).order_by(models.User.coins.desc()).all()
