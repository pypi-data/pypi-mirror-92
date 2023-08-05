import os
import subprocess

from selenium.webdriver import Chrome as _Chrome
from selenium.webdriver import Firefox as _Firefox
from selenium.webdriver import Ie as _Ie
from selenium.webdriver import IeOptions
from selenium.webdriver.remote.remote_connection import RemoteConnection
from urllib3.util import timeout as _timeout

from . import utils
from ..common.utils import get_platform

# 셀레니움이 웹 드라이버의 응답을 받지 못할 경우 무한하게 대기하여 프로그램이 멈추는 현상을 수정합니다.
RemoteConnection.set_timeout(_timeout.Timeout(total=30))


class Chrome(_Chrome):

    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):
        platform, _ = get_platform()

        _, ext = os.path.splitext(executable_path)

        if platform == platform.Windows and ext == '':
            executable_path += '.exe'

        abs_executable_path = os.path.join(os.getcwd(), executable_path)

        if not os.path.exists(abs_executable_path):
            chrome_version = get_chrome_version(platform)
            utils.download_driver(
                "https://chromedriver.storage.googleapis.com/"
                f"{chrome_version}/chromedriver_{platform.value}{64 if platform != platform.Windows else 32}.zip",
                abs_executable_path)

        super().__init__(executable_path=executable_path, port=port, options=options, service_args=service_args,
                         desired_capabilities=desired_capabilities, service_log_path=service_log_path,
                         chrome_options=chrome_options, keep_alive=keep_alive)

        self.implicitly_wait(3)
        self.set_page_load_timeout(15)
        self.set_script_timeout(15)


class Ie(_Ie):

    def __init__(self, executable_path='IEDriverServer.exe', capabilities=None,
                 port=0, timeout=30, host=None,
                 log_level=None, service_log_path=None, options=None,
                 ie_options=None, desired_capabilities=None, log_file=None, keep_alive=False):

        platform, is64bit = get_platform()

        _, ext = os.path.splitext(executable_path)

        if platform == platform.Windows and ext == '':
            executable_path += '.exe'

        abs_executable_path = os.path.join(os.getcwd(), executable_path)

        if not os.path.exists(abs_executable_path):
            utils.download_driver(
                "https://selenium-release.storage.googleapis.com/3.150/IEDriverServer_Win32_3.150.1.zip",
                abs_executable_path)

        if ie_options is None:
            ie_options = IeOptions()

            ie_options.ignore_zoom_level = True
            ie_options.ignore_protected_mode_settings = True
            ie_options.native_events = False
            ie_options.persistent_hover = True

        p = subprocess.Popen(['reg', 'query',
                              "HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\"
                              "Internet Explorer\\Main\\FeatureControl\\FEATURE_BFCACHE",
                              '/v', 'iexplore.exe', '/t', 'REG_DWORD'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, universal_newlines=True)

        if '0x0' not in p.communicate()[0]:

            if is64bit:
                p = subprocess.Popen(['reg', 'add',
                                      'HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\'
                                      'Internet Explorer\\Main\\FeatureControl\\FEATURE_BFCACHE',
                                      '/v', 'iexplore.exe', '/t', 'REG_DWORD', '/d', '0'], stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = p.communicate()
                if p.returncode == 0:
                    print(stdout)
                else:
                    raise Exception(stderr)
            else:
                p = subprocess.Popen(['reg', 'add',
                                      'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\'
                                      'Internet Explorer\\Main\\FeatureControl\\FEATURE_BFCACHE',
                                      '/v', 'iexplore.exe', '/t', 'REG_DWORD', '/d', '0'], stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = p.communicate()
                if p.returncode == 0:
                    print(stdout)
                else:
                    raise Exception(stderr)

        super().__init__(executable_path=executable_path, capabilities=capabilities,
                         port=port, timeout=timeout, host=host,
                         log_level=log_level, service_log_path=service_log_path, options=options,
                         ie_options=ie_options, desired_capabilities=desired_capabilities, log_file=log_file,
                         keep_alive=keep_alive)

        self.implicitly_wait(3)
        self.set_page_load_timeout(15)
        self.set_script_timeout(15)


class Firefox(_Firefox):

    def __init__(self, firefox_profile=None, firefox_binary=None,
                 timeout=30, capabilities=None, proxy=None,
                 executable_path="geckodriver", options=None,
                 service_log_path="geckodriver.log", firefox_options=None,
                 service_args=None, desired_capabilities=None, log_path=None,
                 keep_alive=True):
        platform, is_64bit = get_platform()

        _, ext = os.path.splitext(executable_path)

        if platform == platform.Windows and ext == '':
            executable_path += '.exe'

        abs_executable_path = os.path.join(os.getcwd(), executable_path)

        if not os.path.exists(abs_executable_path):
            utils.download_driver(
                f"https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-"
                f"{platform.value}{64 if is_64bit else 32 if platform != platform.Mac else 'os'}"
                f".{'tar.gz' if platform != platform.Windows else 'zip'}",
                abs_executable_path)

        super().__init__(firefox_profile=firefox_profile, firefox_binary=firefox_binary,
                         timeout=timeout, capabilities=capabilities, proxy=proxy,
                         executable_path=executable_path, options=options,
                         service_log_path=service_log_path, firefox_options=firefox_options,
                         service_args=service_args, desired_capabilities=desired_capabilities, log_path=log_path,
                         keep_alive=keep_alive)

        self.implicitly_wait(3)
        self.set_page_load_timeout(15)
        self.set_script_timeout(15)
