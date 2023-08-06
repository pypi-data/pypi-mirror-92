import asyncio
from biolib.pyppeteer.pyppeteer import launch, command
from biolib.pyppeteer.pyppeteer.launcher import resolveExecutablePath, __chromium_revision__
import http.server
import socketserver
import threading
import base64
import os
import sys
import subprocess
import re
import requests
import logging
import shutil
from pathlib import Path

# fix required for async to work in notebooks
import nest_asyncio
nest_asyncio.apply()

import sys, logging
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                     level=logging.INFO, stream=sys.stdout)
logging.getLogger('biolib.pyppeteer.pyppeteer').setLevel(logging.ERROR)
logging.getLogger('biolib.pyppeteer.pyppeteer.connection').setLevel(logging.ERROR)

biolib_logger = logging.getLogger('biolib')

class BioLibError(Exception):
    def __init__(self, message):
        self.message = message


class CompletedProcess:
    def __init__(self, stdout, stderr, exitcode):
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode

    def ipython_markdown(self):
        from IPython.display import display, Markdown
        markdown_str = self.stdout.decode("utf-8")
        # prepend ./biolib_results/ to all paths
        # ie [SeqLogo](./SeqLogo2.png) test ![SeqLogo](./SeqLogo.png)
        # ![SeqLogo](SeqLogo.png)  ![SeqLogo](/SeqLogo.png)
        # is transformed to ![SeqLogo](./biolib_results/SeqLogo2.png) test ![SeqLogo](./biolib_results/SeqLogo.png)
        # ![SeqLogo](./biolib_results/SeqLogo.png)  ![SeqLogo](./biolib_results/SeqLogo.png)
        markdown_str_modified = re.sub('\!\[([^\]]*)\]\((\.\/|\/|)([^\)]*)\)', '![\\1](./biolib_results/\\3)', markdown_str)
        display(Markdown(markdown_str_modified))

class BioLibServer(socketserver.TCPServer):
    log_level = logging.INFO

class BioLibHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if self.server.log_level == BioLib.TRACE_LOGGING:
            http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)


def js_to_python_byte_array_converter(js_encoded):
    return bytes(list([js_encoded[str(i)] for i in range(len(js_encoded))]))


def python_bytes_to_byte64(data):
    return base64.b64encode(data).decode('ascii')


class BioLib:
    executable_path = None
    no_sandbox = True
    log_level = logging.INFO
    TRACE_LOGGING = 50
    auth_email = None
    auth_password = None
    auth_access_token = None
    auth_refresh_token = None
    host = "https://biolib.com"

    @staticmethod
    def set_chrome_path(path):
        BioLib.executable_path = path

    @staticmethod
    def set_sandbox(use_sandbox):
        BioLib.no_sandbox = not use_sandbox

    @staticmethod
    def set_credentials(email, password):
        BioLib.auth_email = email
        BioLib.auth_password = password

    @staticmethod
    def attempt_login(exit_on_failure=False):
        if BioLib.auth_email is None:
            if exit_on_failure:
                biolib_logger.error("Error: Attempted login, but BIOLIB_EMAIL was not set, exiting...")
                sys.exit(1)
            else:
                biolib_logger.debug("Attempted login, but BIOLIB_EMAIL was not set, so continuing without logging in")
                return
        if BioLib.auth_password is None:
            if exit_on_failure:
                biolib_logger.error("Error: Attempted login, but BIOLIB_PASSWORD was not set, exiting...")
                sys.exit(1)
            else:
                biolib_logger.debug("Attempted login, but BIOLIB_PASSWORD was not set, so continuing without logging in")
                return

        r = requests.post(f"{BioLib.host}/api/user/token/",
                          json={"email": BioLib.auth_email, "password": BioLib.auth_password })
        response = r.json()
        if not r.ok:
            biolib_logger.error(f"Login failed for {BioLib.auth_email}:")
            biolib_logger.error(response["detail"])
            sys.exit(1)
        else:
            BioLib.auth_refresh_token = response["refresh"]
            BioLib.auth_access_token = response["access"]
            biolib_logger.info(f"Successfully authenticated {BioLib.auth_email}")

    @staticmethod
    def push(author_and_app_name, app_path):
        # prepare zip file
        if not Path(f"{app_path}/.biolib/config.yml").is_file():
            biolib_logger.error("The file .biolib/config.yml was not found in the application directory")
            sys.exit(1)
        cwd = os.getcwd()
        os.chdir(app_path)
        zip_name = "biolib-cli-build-tmp-zip-1js7ah2akd"
        zip_filename = f"{zip_name}.zip"
        if Path(zip_filename).is_file():
            biolib_logger.error(f"Please make sure you don't have a file "
                                f"called {zip_filename} in the application directory")
            sys.exit(1)
        shutil.make_archive(zip_name, 'zip', root_dir="..", base_dir=app_path)
        f = open(zip_filename, "rb")
        zip_binary = f.read()
        f.close()
        os.remove(zip_filename)
        # change back to old working directory
        os.chdir(cwd)

        # login and get app data
        BioLib.attempt_login(exit_on_failure=True)
        author_and_app_name_split = author_and_app_name.split("/")
        app = BioLib.get_app_from_author_and_app_name(author_and_app_name_split[0],
                                                      author_and_app_name_split[1])
        # push new app version
        r = requests.post(
            f"{BioLib.host}/api/app_versions/", 
            headers={ "Authorization": f"Bearer {BioLib.auth_access_token}" }, 
            files={
                "app": (None, app["public_id"]),
                "set_as_active": (None, "true"),
                "state": (None, "published"),
                "source_files_zip": zip_binary
            })
        if not r.ok:
            biolib_logger.error(f"Push failed for {author_and_app_name}:")
            biolib_logger.error(r.text)
            sys.exit(1)
        else:
            # TODO: When response includes the version number, print the URL for the new app version
            _response = r.json()
            biolib_logger.info(f"Successfully pushed app version for {author_and_app_name}.")

    @staticmethod
    def get_app_from_author_and_app_name(author_name, app_name):
        headers = {}
        if BioLib.auth_access_token is not None:
            headers["Authorization"] = f"Bearer {BioLib.auth_access_token}"
        r = requests.get(f"{BioLib.host}/api/apps/?account_handle={author_name}&app_name={app_name}",
                         headers=headers)
        results = r.json()['results']
        if len(results) == 0:
            raise Exception(f"Application '{author_name}/{app_name}' was not found. "
                            f"Make sure you have spelled the application name correctly, "
                            f"and that you have the required permissions.")
        return results[0]

    @staticmethod
    def set_logging(log_level):
        BioLib.log_level = log_level
        # only activate debug logging globally if user selected trace logging
        if log_level == BioLib.TRACE_LOGGING:
            logging.getLogger().setLevel(logging.DEBUG)
        elif log_level == logging.DEBUG:
            logging.getLogger().setLevel(logging.INFO)
            biolib_logger.setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(log_level)

    @staticmethod
    def set_host(host):
        if host:
            BioLib.host = host

# set default logging to info
BioLib.set_logging(logging.INFO)

class BioLibApp:

    app_author = None
    app_name = None

    def __init__(self, author, name):
        self.app_author = author
        self.app_name = name

    async def call_pyppeteer(self, port, args, stdin, files, output_path):
        if not BioLib.executable_path:
            mac_chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if os.path.isfile(mac_chrome_path):
                BioLib.set_chrome_path(mac_chrome_path)

        if not BioLib.executable_path:
            linux_chrome_path = "/usr/lib/chromium-browser/chromium-browser"

            # special install for google colab
            if not os.path.isfile(linux_chrome_path) and 'google.colab' in sys.modules:
                subprocess.run("apt-get update", shell=True, check=True)
                subprocess.run("apt install chromium-chromedriver", shell=True, check=True)

            if os.path.isfile(linux_chrome_path):
                BioLib.set_chrome_path(linux_chrome_path)

        resolved_path = resolveExecutablePath(None, __chromium_revision__)
        if not BioLib.executable_path and resolved_path[1]:
            # if executable_path is not set explicit,
            # and resolveExecutablePath failed (== we got an error message back in resolved_path[1])
            logging.info("Installing dependencies...")
            os.environ['PYPPETEER_NO_PROGRESS_BAR'] = "true"
            command.install()

        logging.info("Computing...")

        chrome_arguments = [
                '--disable-web-security',
            ]
        if BioLib.no_sandbox:
            chrome_arguments.append('--no-sandbox')

        browser = await launch(args=chrome_arguments, executablePath=BioLib.executable_path)

        # start new page
        page = await browser.newPage()

        await page.goto("http://localhost:" + str(port))

        def getCode():
            return python_bytes_to_byte64(b"code")

        def getData():
            data = {}
            data["stdin"] = stdin
            data["parameters"] = args
            data["files"] = files
            return data

        def setProgressCompute(x):
            biolib_logger.debug(f"Compute progress: {x}")

        def setProgressInitialization(x):
            biolib_logger.debug(f"Initialization progress: {x}")

        def addLogMessage(x):
            biolib_logger.debug(f"Log message: {x}")

        await page.exposeFunction("getCode", getCode)
        await page.exposeFunction("getData", getData)
        await page.exposeFunction("setProgressCompute", setProgressCompute)
        await page.exposeFunction("setProgressInitialization", setProgressInitialization)
        await page.exposeFunction("addLogMessage", addLogMessage)

        refreshToken = "undefined"
        if BioLib.auth_refresh_token:
            refreshToken = f"\"{BioLib.auth_refresh_token}\""

        result = await page.evaluate("""
        async function() {
          const refreshToken = """+refreshToken+""";
          window.BioLib.BioLibSingleton.setConfig({ baseUrl: \"""" + BioLib.host + """\", refreshToken });
          window.BioLib.AppClient.setApiClient(window.BioLib.BioLibSingleton.get());
          var data = await window.getData()
          data["stdin"] = Uint8Array.from(atob(data["stdin"]), c => c.charCodeAt(0))
          for(var i = 0; i<data["files"].length; i++) {
              data["files"][i].data = Uint8Array.from(atob(data["files"][i].data), c => c.charCodeAt(0))
          }
          var jobUtils = {}
          jobUtils["setProgressCompute"] = window.setProgressCompute
          jobUtils["setProgressInitialization"] = window.setProgressInitialization
          jobUtils["addLogMessage"] = window.addLogMessage

          try {
            return await window.BioLib.AppClient.runApp(""" + f"\"{self.app_version_uuid}\",\"{self.semantic_version}\"" + """, data, jobUtils)
          } catch(err) {
            return err.toString()
          }
        }
        """)
        logging.debug("Closing browser")
        await browser.close()

        if isinstance(result, dict):
            if len(result["files"]) > 0:
                logging.info(f"Writing output files to: {output_path}")
                os.makedirs(output_path, exist_ok=True)
                for f in result["files"]:
                    filename = output_path + f["pathWithoutFilename"] + f["name"]
                    data = js_to_python_byte_array_converter(f["data"])
                    fp = open(filename, "wb")
                    fp.write(data)
                    fp.close()
            return CompletedProcess(
                stdout=js_to_python_byte_array_converter(result["stdout"]),
                stderr=js_to_python_byte_array_converter(result["stderr"]),
                exitcode=result["exitcode"]
            )
        else:
            raise BioLibError(result)

    def __call__(self, args=[], stdin=None, files=None, output_path="biolib_results"):
        BioLib.attempt_login()
        logging.info("Loading package...")
        app = BioLib.get_app_from_author_and_app_name(self.app_author, self.app_name)
        self.app_version_uuid = app["public_id"]
        self.semantic_version = f"{app['active_version']['major']}.{app['active_version']['minor']}.{app['active_version']['patch']}"
        logging.info(f"Loaded package: {self.app_author}/{self.app_name}")

        cwd = os.getcwd()

        if stdin is None:
            stdin = b""

        if not output_path.startswith("/"):
            # output_path is relative, make absolute
            output_path = f"{cwd}/{output_path}"

        if isinstance(args, str):
            args = list(filter(lambda p: p != "", args.split(" ")))

        if not isinstance(args, list):
            raise Exception("The given input arguments must be list or str")

        if isinstance(stdin, str):
            stdin = stdin.encode("utf-8")

        if files is None:
            files = []
            for idx, arg in enumerate(args):
                if os.path.isfile(arg):
                    files.append(arg)
                    args[idx] = arg.split("/")[-1]

        files_data = []
        for f in files:
            path = f
            if not f.startswith("/"):
                # make path absolute
                path = cwd + "/" + f

            arg_split = path.split("/")
            file = open(path, "rb")
            files_data.append({
                "pathWithoutFilename": "/",
                "name": arg_split[-1],
                "data": python_bytes_to_byte64(file.read())
            })
            file.close()

        stdin = python_bytes_to_byte64(stdin)

        BioLibServer.log_level = BioLib.log_level
        with BioLibServer(("127.0.0.1", 0), BioLibHandler) as httpd:
            port = httpd.server_address[1]
            thread = threading.Thread(target=httpd.serve_forever)
            # TODO: figure out how we can avoid changing the current directory
            os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/biolib-js/")
            try:
                thread.start()
                res = asyncio.get_event_loop().run_until_complete(
                    self.call_pyppeteer(port=port, args=args, stdin=stdin, files=files_data, output_path=output_path))
            finally:
                os.chdir(cwd)
            httpd.shutdown()
            thread.join()
            return res

        raise BioLibError("Failed to start TCPServer")
