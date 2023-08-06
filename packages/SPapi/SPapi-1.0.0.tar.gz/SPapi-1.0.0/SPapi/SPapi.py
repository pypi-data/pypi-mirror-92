'''
Модуль для работы с сайтом серверов СП, подходит для использования при создании Дискорд ботов и других программ на Python.

By Spagetik
'''

from requests import post, Response


class Private():

    def byte_to_text(response: Response):
        response.encoding = 'utf-8'
        return response.text

    def send_response(response: Response, byte_inf):
        if byte_inf == False:
            return Private.byte_to_text(response)
        elif byte_inf == True:
            return response
        else:
            return response.json()


def test(token, server='spk', byte_inf=None):
    """Отправка тестового запроса. Проверка работоспособности.

    :param token: Токен вашего приложения.

    :param server: *Сервер, для которого делается приложение: 'sp' - СП; 'spm' - СПм; 'spk' - СПк. Дефолтное значение: 'spk'.

    :param byte_inf: *Тип возвращаемых данных: None - dict(); True - byte(); False - str(). Дефолтное значение - None.

    :return: Возвращает ответ от сервера в выбраном виде (Подроебнее в документации на сайте).
    """
    response = post(f'https://{server}.jakksoft.com/api/request', data={'token':token, 'action':'test'})
    return Private.send_response(response=response, byte_inf=byte_inf)


def permission_test(token, license_key, server='spk', byte_inf=None):
    ''' Тест прав-доступа, работает ТОЛЬКО С ВАШИМ КЛЮЧОМ!

    :param token: Токен вашего приложения

    :param license_key: ВАШ ключ-лицензия со страницы /settings#collapseApps

    :param server: *Сервер, для которого делается приложение: 'sp' - СП; 'spm' - СПм; 'spk' - СПк. Дефолтное значение: 'spk'.

    :param byte_inf: *Тип возвращаемых данных: None - dict(); True - byte(); False - str(). Дефолтное значение - None.

    :return: Возвращает ответ от сервера в выбраном виде (Подроебнее в документации на сайте).
    '''
    response = post(f'https://{server}.jakksoft.com/api/request', data={'token':token, 'action':'permission_test', 'license_key':license_key})
    return Private.send_response(response=response, byte_inf=byte_inf)


def pay(token, spPayCode, sum, transactionMessage='Оплата услуги через SP-pay', server='spk', byte_inf=None):
    '''Прием оплаты через SP-pay

    :param token: Токен вашего приложения.

    :param spPayCode: Код SP-pay созданый покупателем на сайте.

    :param sum: Сумма оплаты. ВНИМАНИЕ! Сумма при созданнии кода и этот параметр ДОЛЖНЫ БЫТЬ ОДИНАКОВЫМИ, ичначе вылетит ошибка!

    :param transactionMessage: *Сообщение с переводом. Дефолтное значение - 'Оплата услуги через SP-pay'

    :param server: *Сервер, для которого делается приложение: 'sp' - СП; 'spm' - СПм; 'spk' - СПк. Дефолтное значение: 'spk'.

    :param byte_inf: *Тип возвращаемых данных: None - dict(); True - byte(); False - str(). Дефолтное значение - None.

    :return: Возвращает ответ от сервера в выбраном виде (Подроебнее в документации на сайте).
    '''
    response = post(f'https://{server}.jakksoft.com/api/request', data={'token':token, 'action':'pay', 'spPayCode':spPayCode, 'sum':sum, 'transactionMessage':transactionMessage})
    return Private.send_response(response=response, byte_inf=byte_inf)


def get_permission(token, license_key, permission_id, server='spk', byte_inf=None):
    '''Оправка запроса на получение прав.

    :param token: Токен вашего приложения.

    :param license_key: Ключ-лицензия игрока, у которого запрашиваются права доступа.

    :param permission_id: Право на которое запрашивается доступ: 1 - Тестовое разрешение; 2 - Чтение информации о банковских счетах; 3 - Чтение уведомлений; 4 - Пометка уведомлений прочитанными

    :param server: *Сервер, для которого делается приложение: 'sp' - СП; 'spm' - СПм; 'spk' - СПк. Дефолтное значение: 'spk'.

    :param byte_inf: *Тип возвращаемых данных: None - dict(); True - byte(); False - str(). Дефолтное значение - None.

    :return: Возвращает ответ от сервера в выбраном виде (Подроебнее в документации на сайте).
    '''
    response = post(f'https://{server}.jakksoft.com/api/request', data={'token':token, 'action':'get_permission', 'license_key':license_key, 'permission_id':permission_id})
    return Private.send_response(response=response, byte_inf=byte_inf)


def get_cards_info(token, license_key, server='spk', byte_inf=None):
    '''Запрос информации о картах пользователя.

    :param token: Токен вашего приложения.

    :param license_key: Ключ-лицензия игрока, у которого запрашиваются права доступа.

    :param server: *Сервер, для которого делается приложение: 'sp' - СП; 'spm' - СПм; 'spk' - СПк. Дефолтное значение: 'spk'.

    :param byte_inf: *Тип возвращаемых данных: None - dict(); True - byte(); False - str(). Дефолтное значение - None.

    :return: Возвращает ответ от сервера в выбраном виде (Подроебнее в документации на сайте).
    '''
    response = post(f'https://{server}.jakksoft.com/api/request', data={'token':token, 'action':'get_cards_info', 'license_key':license_key})
    return Private.send_response(response=response, byte_inf=byte_inf)


def get_unread_notifications(token, license_key, server='spk', byte_inf=None):
    '''Получение непрочитаных (новых) уведомлений пользователя.

    :param token: Токен вашего приложения.

    :param license_key: Ключ-лицензия игрока, у которого запрашиваются права доступа.

    :param server: *Сервер, для которого делается приложение: 'sp' - СП; 'spm' - СПм; 'spk' - СПк. Дефолтное значение: 'spk'.

    :param byte_inf: *Тип возвращаемых данных: None - dict(); True - byte(); False - str(). Дефолтное значение - None.

    :return: Возвращает ответ от сервера в выбраном виде (Подроебнее в документации на сайте).
    '''
    response = post(f'https://{server}.jakksoft.com/api/request', data={'token':token, 'action':'get_unread_notifications', 'license_key':license_key})
    return Private.send_response(response=response, byte_inf=byte_inf)


def  mark_notifications_as_read(token, license_key, server='spk', byte_inf=None):
    '''Отметка уведомления как прочитаного.

    :param token: Токен вашего приложения.

    :param license_key: Ключ-лицензия игрока, у которого запрашиваются права доступа.

    :param server: *Сервер, для которого делается приложение: 'sp' - СП; 'spm' - СПм; 'spk' - СПк. Дефолтное значение: 'spk'.

    :param byte_inf: *Тип возвращаемых данных: None - dict(); True - byte(); False - str(). Дефолтное значение - None.

    :return: Возвращает ответ от сервера в выбраном виде (Подроебнее в документации на сайте).
    '''
    response = post(f'https://{server}.jakksoft.com/api/request', data={'token':token, 'action':'mark_notifications_as_read', 'license_key':license_key})
    return Private.send_response(response=response, byte_inf=byte_inf)
