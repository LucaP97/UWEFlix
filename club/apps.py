from django.apps import AppConfig


class ClubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'club'

    # def ready(self) -> None:
    #     print('club app ready executed')
    #     import club.signals
    #     # return super().ready()
