from telegram_bot_calendar import DetailedTelegramCalendar


class User:
    users = dict()

    def __init__(self, id):
        self.id = id
        User.add_user(id, self)
        self.search_data = []
        self.answer = []

    @classmethod
    def add_user(cls, id, user):
        cls.users[id] = user

    @classmethod
    def get_user(cls, id):
        if id not in cls.users.keys():
            a = cls(id)
            return a
        else:
            return cls.users[id]


class MyTranslationCalendar(DetailedTelegramCalendar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days_of_week['ru'] = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        self.months['ru'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                                  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']