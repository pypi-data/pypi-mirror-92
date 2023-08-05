import asyncio
import threading
from abc import ABCMeta, abstractmethod

import mitmproxy.http
import mitmproxy.tcp
import mitmproxy.websocket
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster


class Proxy:

    def __init__(self, listen_host='0.0.0.0', listen_port=8080, http2=True, **kwargs):
        options = Options(listen_host=listen_host, listen_port=listen_port, http2=http2, **kwargs)
        self.dump_master = DumpMaster(options, with_termlog=False, with_dumper=False)
        self.dump_master.server = ProxyServer(ProxyConfig(options))
        self.proxy_thread = threading.Thread(target=self._run_loop, args=(asyncio.get_event_loop(),))

    def add_addon(self, addon):
        self.dump_master.addons.add(addon)

    def remove_addon(self):
        self.dump_master.addons.remove()

    def _run_loop(self, loop):
        exc = None
        try:
            loop.run_forever()
        except Exception:  # pragma: no cover
            exc = traceback.format_exc()
        finally:
            if not self.dump_master.should_exit.is_set():  # pragma: no cover
                self.dump_master.shutdown()
            tasks = asyncio.all_tasks(loop)
            for p in tasks:
                p.cancel()
            loop.close()

        if exc:  # pragma: no cover
            print(exc, file=sys.stderr)
            print("mitmproxy has crashed!", file=sys.stderr)
            print("Please lodge a bug report at:", file=sys.stderr)
            print("\thttps://github.com/mitmproxy/mitmproxy", file=sys.stderr)

        self.dump_master.addons.trigger("done")

    def _run(self):
        self.dump_master.start()
        asyncio.ensure_future(self.dump_master.running())

    def start(self):
        self._run()
        self.proxy_thread.start()

    def stop(self):
        self.dump_master.shutdown()
