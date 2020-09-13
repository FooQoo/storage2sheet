from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class SheetAPI:
    """
    memcacheとやり取りするAPI

    Attributes
    -------
    GOOGLE_PATH : str
        キャッシュのキー
    KEY_FILE : str
        サービスアカウント情報が記載されたローカルのパス
    MIME_TYPE : str
        ファイル形式
    file_key : str
        google driveのフォルダーのキー
    service : service
        gcpのサービスアカウント
    """

    def __init__(self, service_account_key_path: str, sheet_id: str):
        """
        コンストラクタ

        Parameters
        ----------
        service_account_key_path : str
            サービスアカウントのキー情報が記載されたローカルパス
        sheet_id : str
            spreadsheetのキー
        """

        self.GOOGLE_PATH = 'https://www.googleapis.com/auth/spreadsheets'
        self.KEY_FILE = service_account_key_path
        self.service = self.__get_google_service()
        self.SHEET_ID = sheet_id

    def append(self, cells: list):
        """
        google spread sheetに行追加

        Parameters
        ----------
        cells : str
            ファイルの内容(銘柄情報のcsvフォーマット)
        """

        data = [
            {
                'range': 'A1',
                'values': cells
            },
        ]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.SHEET_ID, body=body).execute()

    def __get_google_service(self):
        """
        gcpのサービスアカウントの取得

        Returns
        -------
        service
            サービスアカウントクラス
        """
        scope = [self.GOOGLE_PATH]
        key_file = self.KEY_FILE
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file, scopes=scope)

        return build(
            "sheets",
            "v4",
            credentials=credentials,
            cache_discovery=False)
