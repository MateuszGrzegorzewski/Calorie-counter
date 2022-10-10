from database import db
import datetime


class TimeModel(db.Model):
    __tablename__ = 'time'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100)) 
    mealtimes = db.relationship('DailyMealsModel', backref='time', lazy='joined')

    def __init__(self, date):
        self.date = date

    def save_dates_to_db():
        start = datetime.datetime.strptime("2022-10-01", "%Y-%m-%d")
        end = datetime.datetime.strptime("2022-10-30", "%Y-%m-%d")
        date_generated = (start + datetime.timedelta(days=x)
                          for x in range(0, (end-start).days + 1))

        for date in date_generated:
            db.session.add(TimeModel(date.strftime("%Y-%m-%d")))
            db.session.commit()
