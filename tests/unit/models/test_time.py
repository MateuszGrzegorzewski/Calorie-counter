from main import create_app
from models.time import TimeModel


class TestTimeModel():
    def test_create_time_model(self):
        time = TimeModel('2022-12-13')

        assert time is not None
        assert time.date == '2022-12-13'
