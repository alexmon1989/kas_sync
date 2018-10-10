import requests
import pyodbc
import configparser
import logging


def get_claims_without_number():
    """Получение идентификаторов новых заявок без номера."""
    r = requests.get(f"{API_URL}/claims/raw-claim-ids")
    return r.json()


def get_gloc_next_number(muc_id):
    """Получает новый (следующий) номер для заявки из GLOC."""
    cnxn = pyodbc.connect(GLOC_CONNECTION_STRING)
    cursor = cnxn.cursor()
    sql = """\
        SET NOCOUNT ON
        DECLARE @out NVARCHAR ( max )
        EXEC GLOC.ext.GetNumeratorNextNumber @idNumerator = ?, @number = @out OUTPUT
        SELECT @out AS result
        """
    params = (muc_id,)
    cursor.execute(sql, params)
    row = cursor.fetchone()
    cnxn.commit()
    cnxn.close()
    number = row[0]
    return number


def set_claim_numbers():
    """Присвоение заявкам номеров из GLOC."""
    # Получение неподписанных заявок без номера
    logging.info("Присвоение заявкам номеров из GLOC")
    logging.info("Получение новых заявок без номера")
    claims = get_claims_without_number()
    logging.info(f"Список новых заявок без номера успешно получен (количество: {len(claims)})")

    # Получение номера из ГЛОК и формирование данных для запроса на API
    data = []
    for claim in claims:
        logging.info(
            f"Получение нового номера для заявки из GLOC (claim_id = {claim['claim_id']}, muc={claim['muc_id']})")
        number = get_gloc_next_number(claim['muc_id'])
        logging.info(f"Получен номер {number}.")

        data.append({
            'claim_id': claim['claim_id'],
            'glok_id': number
        })

    # Запрос на API
    logging.info("Отправка запроса на присвоение заявкам номеров из GLOC")
    requests.post(f"{API_URL}/claims/raw-claim-ids", json=data)
    logging.info("Присвоение заявкам номеров из GLOC успешно завершено")


def get_claims_ids_signed():
    """Получает список идентификаторов новых (подписанных ЭЦП) заявок с номером."""
    r = requests.get(f"{API_URL}/claims/new-claims")
    return r.json()


def complete_claims():
    """Помечает заявки как обработанные."""
    logging.info("Обработка новых (подписанных ЭЦП) заявок с номером")
    logging.info("Получение списка новых (подписанных ЭЦП) заявок с номером")
    claims = get_claims_ids_signed()
    logging.info(f"Список новых (подписанных ЭЦП) заявок с номером успешно получен (количество: {len(claims)})")

    for claim in claims:
        # TODO: Что-то происходит (запись в БД, копирование файлов)
        pass

    logging.info("Отправка запроса на пометку заявок как синхронизированных")
    requests.post(f"{API_URL}/claims/new-claims", json=claims)
    logging.info("Пометка заявок как синхронизированных успшено завершена")
    logging.info("Обработка новых (подписанных ЭЦП) заявок с номером успшено завершена")


def main():
    # Присвоение номера новым заявкам
    set_claim_numbers()

    # Обработка подписанных заявок с номером
    complete_claims()


if __name__ == "__main__":
    # Считывание основных настроек
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # Web-адрес API
    API_URL = config['API']['URL']
    # Строка подключения к БД КАС
    KAS_CONNECTION_STRING = config['DB']['KAS_CONNECTION_STRING']
    # Строка подключения к БД ГЛОК
    GLOC_CONNECTION_STRING = config['DB']['GLOC_CONNECTION_STRING']

    logging.basicConfig(filename="logfile.log", level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info("Старт программы")

    # Вызов основной функции
    main()

    logging.info("Завершение программы")
