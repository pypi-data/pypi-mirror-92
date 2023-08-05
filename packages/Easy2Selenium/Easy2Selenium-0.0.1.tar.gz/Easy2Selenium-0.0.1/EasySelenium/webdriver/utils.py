import subprocess
from io import BytesIO
from urllib import request

from EasySelenium.common.utils import OsName


def download_driver(url: str, save_path: str) -> None:
    with request.urlopen(url) as res:
        if url.split(".")[-1] == "zip":
            import zipfile
            zip_f = zipfile.ZipFile(BytesIO(res.read()))
            with open(save_path, 'wb') as f:
                f.write(zip_f.read(zip_f.namelist()[-1]))
        else:
            import tarfile
            zip_f = tarfile.open(fileobj=BytesIO(res.read()), mode='r:gz')
            with open(save_path, 'wb') as f:
                f.write(zip_f.extractfile(zip_f.getmember(zip_f.getnames()[-1])).read())


def get_chrome_version(os_name: OsName) -> str:
    if os_name == OsName.Linux:
        pass
    elif os_name == OsName.Windows:
        stdout = subprocess.check_output(
            ["reg", "query", "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon", "/v", "version"])
        return stdout.decode().strip().split()[-1]
    elif os_name == OsName.Mac:
        pass
