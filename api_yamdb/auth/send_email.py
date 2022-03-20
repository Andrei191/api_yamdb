from django.core import mail


def send_mail():
    mail.send_mail(
        'Confirmation code',
        '12345',
        'from@example.com',
        [request.data['email']],
    )

# можно заставить это работать из этого файла и будет красиво,
# но хз как вытащить из сериализатора почту..)
