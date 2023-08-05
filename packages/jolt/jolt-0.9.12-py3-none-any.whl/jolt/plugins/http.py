import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectTimeout, RequestException
import keyring
import getpass


from jolt import utils
from jolt import cache
from jolt import log
from jolt import config
from jolt import filesystem as fs
from jolt.error import raise_error_if, JoltError


NAME = "http"
TIMEOUT = (3.5, 27)
TIMEOUT_HEAD = (27, 27)


class Http(cache.StorageProvider):
    def __init__(self, cache):
        super(Http, self).__init__()
        self._cache = cache
        self._uri = config.get(NAME, "uri")
        raise_error_if(not self._uri, "HTTP URI not configured")
        if self._uri[-1] != "/":
            self._uri += "/"
        self._upload = config.getboolean(NAME, "upload", True)
        self._download = config.getboolean(NAME, "download", True)
        self._disabled = False

    def _get_auth(self):
        service = config.get(NAME, "keyring.service")
        if not service:
            return None

        username = config.get(NAME, "keyring.username")
        if not username:
            username = utils.read_input(NAME + " username: ")
            raise_error_if(not username, "no username configured for " + NAME)
            config.set(NAME, "keyring.username", username)
            config.save()

        password = config.get(NAME, "keyring.password") or \
                   keyring.get_password(NAME, username)
        if not password:
            password = getpass.getpass(NAME + " password: ")
            raise_error_if(not password, "no password in keyring for " + NAME)
            keyring.set_password(service, username, password)
        return HTTPBasicAuth(username, password)

    def _get_url(self, node, artifact):
        return "{uri}/{name}/{file}".format(
            uri=self._uri,
            name=node.name,
            file=fs.path.basename(artifact.get_archive_path()))

    @utils.retried.on_exception((RequestException, JoltError))
    def download(self, node, force=False):
        if self._disabled:
            return False
        if not self._download and not force:
            return False
        with self._cache.get_artifact(node) as artifact:
            url = self._get_url(node, artifact)
            if node.tools.download(url, artifact.get_archive_path(), exceptions=True, timeout=TIMEOUT):
                return True
        return False

    def download_enabled(self):
        return not self._disabled and self._download

    @utils.retried.on_exception((RequestException))
    def upload(self, node, force=False):
        if self._disabled:
            return True
        if not self._upload and not force:
            return True
        with self._cache.get_artifact(node) as artifact:
            url = self._get_url(node, artifact)
            archive = artifact.get_archive()
            return node.tools.upload(archive, url, exceptions=True,
                                     auth=self._get_auth(), timeout=TIMEOUT)
        return False

    def upload_enabled(self):
        return not self._disabled and self._upload

    @utils.retried.on_exception((RequestException))
    def location(self, node):
        if self._disabled:
            return False
        with self._cache.get_artifact(node) as artifact:
            url = self._get_url(node, artifact)
            try:
                response = requests.head(url, stream=True, timeout=TIMEOUT_HEAD)
            except ConnectTimeout:
                self._disabled = True
                log.warning("[HTTP] failed to establish server connection, disabled")
                return False

            log.debug("[HTTP] Head: {0}", url)
            log.debug("[HTTP] Response: {0}", response.status_code)
            return url if response.status_code == 200 else ''
        return False


@cache.RegisterStorage
class HttpFactory(cache.StorageProviderFactory):
    @staticmethod
    def create(cache):
        log.verbose("[Http] Loaded")
        return Http(cache)
