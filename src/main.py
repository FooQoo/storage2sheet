from os import environ
from dotenv import load_dotenv
from runner import Runner

config = 'resources/.env'
load_dotenv(config, verbose=True)


def main(event, context):
    """
    google functionで実行される関数

    Parameters
    ----------
    event : event
        event情報
    context : context
        context情報
    """
    service_account_key_path = environ.get('SERVICE_ACCOUNT_KEY_PATH')
    backet_id = environ.get('BACKET_ID')
    filename = environ.get('FILENAME')
    sheet_id = environ.get('SHEET_ID')
    runner = Runner(backet_id, filename,
                    service_account_key_path, sheet_id)
    runner.start()


if __name__ == '__main__':
    main(None, None)
