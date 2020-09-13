from repository.sheet import SheetAPI
from repository.storage import StorageAPI
import traceback
from io import StringIO
import pandas as pd

from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

"""
logger: https://qiita.com/amedama/items/b856b2f30c2f38665701
"""


class Runner:
    """
    タスクを実行するクラス

    Attributes
    -------
    YEARS: list
        対象年度を格納したリスト
    CSV_HEADER: str
        CSVのヘッダー
    memcache_api : MemcachedAPI
        キャッシュAPIのインスタンス
    stock_list_api : StockListAPI
        株価リストAPIのインスタンス
    stock_api : KabuojiAPI
        株価取得APIのインスタンス
    drive_api: GoogleDriveAPI
        google driveのAPIのインスタンス
    """

    def __init__(
            self,
            backet_name,
            filename,
            service_account_key_path: str,
            sheet_id: str):
        """
        コンストラクタ

        Parameters
        ----------
        backet_name : str
            バケット名
        filename : str
            ファイル名
        service_account_key_path : str
            google service accountのキーファイルがあるローカルのファイルパス
        sheet_id : str
            スプレッドシートのid
        """
        self.storage_api = StorageAPI(backet_name, filename)
        self.sheet_api = SheetAPI(service_account_key_path, sheet_id)

    def start(self):
        """
        タスクの実行
        """
        try:
            csv = self.__fetch_stock()
            self.__update_sheet(csv)
        except Exception:
            logger.error(traceback.format_exc())
            exit()

    def __fetch_stock(self):
        """
        銘柄情報の取得

        Parameters
        ----------
        code : str
            銘柄コード

        Returns
        -------
        str
            銘柄に関わるcsvフォーマットの文字列
        """
        csv = self.storage_api.get_file_content()

        df = pd.read_csv(StringIO(csv)).sort_index()

        return df.values.tolist()

    def __update_sheet(self, csv):
        self.sheet_api.append(csv)
