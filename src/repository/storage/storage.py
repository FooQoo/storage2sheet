from google.cloud import storage


class StorageAPI:
    """
    GCSとやり取りするAPI
    """

    def __init__(self, backet_name: str, filename: str):
        """コンストラクタ

        Parameters
        ----------
        backet_name : str
            バケット名
        filename : str
            ファイル名
        """
        self.client = storage.Client()
        self.backet_name = backet_name
        self.filename = filename

    def get_file_content(self):
        """ファイルの中身を取得する

        Returns
        -------
        str
            ファイルの中身
        """
        bucket = self.client.get_bucket(self.backet_name)

        if bucket.exists():
            blob = bucket.blob(self.filename)
            return blob.download_as_string().decode()
        else:
            return ""
