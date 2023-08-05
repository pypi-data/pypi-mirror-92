# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import gzip
import lzma
import os
import re
import logging
import sqlite3
import zlib
import json
import datetime
import time

try:
    from systemd import journal

    journal_installed = True
except ImportError:
    journal_installed = False

from typing import Callable, Union, BinaryIO, Sequence, List, Generator, Tuple
from logreduce.data import LogObject, FileLike
from logreduce.tokenizer import Tokenizer


# Avoid those files that aren't useful for words analysis
DEFAULT_IGNORE_PATHS = [
    "zuul-info/",
    "_zuul_ansible/",
    "ara[_-]*.*/",
    "etc/hostname",
    "etc/nodepool/provider",
    # sf-ci useless static files
    "executor.*/trusted/",
    # tripleo-ci static files
    "etc/selinux/targeted/",
    "etc/sysconfig/",
    "etc/systemd/",
    "etc/polkit-1/",
    "etc/pki/",
    r"etc/swift/.*\.builder",
    "group_vars/all.yaml",
    "keystone/credential-keys",
    "keystone/fernet-keys",
    # extra/logstash is already printed in deploy logs
    "extra/logstash.txt",
    "migration/identity.gz",
    "swift/backups/",
    "/conf.modules.d/",
    "/lib/heat-config/heat-config-script/",
    r"\.git/",
    r"\.svn/",
    "/proc/net/",
    r"plugin-suse_.*\.txt",
]

DEFAULT_IGNORE_FILES = [
    "btmp.txt",
    "cpuinfo.txt",
    "devstack-gate-setup-host.txt",
    "df.txt",
    "dstat.txt",
    "free.txt",
    "heat-deploy-times.log.txt",
    "host_info.txt",
    "hosts.txt",
    "id_rsa",
    "index.html",
    "iostat.txt",
    "iotop.txt",
    "lastlog",
    "last",
    "authkey",
    "lsmod.txt",
    "lsof.txt",
    "lsof_network.txt",
    "meminfo.txt",
    "nose_results.html",
    "passwords.yml",
    "postci.txt",
    "pstree.txt",
    "ps.txt",
    "rdo-trunk-deps-end.txt",
    "repolist.txt",
    "service_configs.json.txt",
    "sysctl.txt",
    "sysstat.txt",
    "tempest.log.txt",
    "tempest_output.log.txt",
    "uname.txt",
    "worlddump-",
    "wtmp.txt",
    "README",
    "unbound.log",
    "dns_cache.txt",
    "password.gz",
    "moduli",
    "screen-dstat",
    "atop.bin",
    "log-size.txt",
]

BLACKLIST_EXTENSIONS = (
    ".conf",
    ".conf.txt",
    ".crt",
    ".csr",
    ".css",
    ".db",
    ".ico",
    ".journal",
    ".js",
    ".json",
    ".json.txt",
    "_key",
    ".key",
    ".pcap.log",
    ".pem",
    ".png",
    ".pyc",
    ".pyo",
    "ring.gz",
    ".raw",
    ".rpm",
    ".so",
    ".sqlite",
    ".subunit",
    ".svg",
    ".tgz",
    ".tar",
    ".ttf",
    ".woff",
    ".xml",
    ".yaml",
    ".yaml.txt",
    ".yml",
)

FACILITY2NAME = {
    0: "kern",
    1: "user",
    2: "mail",
    3: "daemon",
    4: "auth",
    5: "syslog",
    6: "lprlog",
    7: "news",
    8: "uucp",
    9: "clock",
    10: "authpriv",
    11: "ftplog",
    12: "unknown",
    13: "unknown",
    14: "unknown",
    15: "cron",
    16: "local0",
    17: "local1",
    18: "local2",
    19: "local3",
    20: "local4",
    21: "local5",
    22: "local6",
    23: "local7",
}


# An adapter function for the legacy keep_file behaviors
def keep_file(
    exclude_files: List[str], exclude_paths: List[str]
) -> Callable[[str], bool]:
    # The function returns False for excluded path
    def fun(path: str) -> bool:
        basename = os.path.basename(path)
        excluded_file = any([True for ign in exclude_files if re.match(ign, basename)])
        excluded_path = any([True for ign in exclude_paths if re.search(ign, path)])
        return not excluded_file and not excluded_path

    return fun


# An adapter function for the legacy exclude_line behavior
def process_line(exclude_lines: List[str]) -> Callable[[str], str]:
    exclude_lines_re = re.compile(r"|".join(exclude_lines)) if exclude_lines else None

    def fun(line: str) -> str:
        if exclude_lines_re and exclude_lines_re.match(line):
            return ""
        return Tokenizer.process(line)

    return fun


class Journal(FileLike):
    def __init__(self, since, previous=False):
        if not journal_installed:
            raise RuntimeError("Please run dnf install -y python3-systemd to continue")
        _day = 3600 * 24
        if since.lower() == "day":
            ts = _day
        elif since.lower() == "week":
            ts = 7 * _day
        elif since.lower() == "month":
            ts = 30 * _day
        else:
            raise RuntimeError("%s: Unknown since timestamp" % since)
        if previous:
            self.name = "last %s" % since
            self.since = time.time() - ts * 2
            self.until = self.since + ts
        else:
            self.name = "this %s" % since
            self.since = time.time() - ts
            self.until = None

    def open(self):
        self.journal = journal.Reader()
        self.journal.seek_realtime(self.since)

    def close(self):
        self.journal.close()
        del self.journal

    def __next__(self):
        entry = self.journal.get_next()
        ts = entry.get("__REALTIME_TIMESTAMP", datetime.datetime(1970, 1, 1))
        if not entry or (self.until and ts.timestamp() > self.until):
            raise StopIteration
        facility = entry.get("SYSLOG_FACILITY")
        if isinstance(facility, int):
            entry["LEVEL"] = FACILITY2NAME.get(facility, "NOTI").upper()
        else:
            entry["LEVEL"] = str(facility)
        entry["DATE"] = ts.strftime("%Y-%m-%d %H:%M:%S")
        entry.setdefault("SYSLOG_IDENTIFIER", "NONE")
        entry.setdefault("MESSAGE", "NONE")
        return "{DATE} - {SYSLOG_IDENTIFIER} - {LEVEL} - {MESSAGE}\n".format(
            **entry
        ).encode("utf-8")

    def __str__(self):
        return "Journal of %s" % self.name


class AraReport(FileLike):
    def __init__(self, db_path):
        self.db_path = db_path
        self.lines = []
        self.idx = 0

    def __next__(self):
        if self.idx >= len(self.lines):
            raise StopIteration
        self.idx += 1
        return self.lines[self.idx - 1].encode("utf-8")

    def open(self):
        con = sqlite3.connect(self.db_path)
        c = con.cursor()
        c.execute(
            "SELECT playbooks.path, tasks.name, task_results.status, "
            "task_results.result"
            " FROM task_results"
            " INNER JOIN tasks ON tasks.id == task_results.task_id"
            " INNER JOIN playbooks ON tasks.playbook_id == playbooks.id"
        )
        result_ignores = ("src", "ansible_facts", "stdout_lines", "stderr_lines")
        for row in c:
            path, name, status, res = row
            res_dec = zlib.decompress(res).decode("utf-8", errors="ignore")
            stdout, stderr = None, None
            try:
                obj = json.loads(res_dec)
                if "cmd" in obj:
                    obj["cmd"] = " ".join(obj["cmd"])
                for ignore in result_ignores:
                    if ignore in obj:
                        del obj[ignore]
                if "stdout" in obj:
                    stdout = obj["stdout"]
                    del obj["stdout"]
                if "stderr" in obj:
                    stderr = obj["stderr"]
                    del obj["stderr"]
                result = []
                for k, v in sorted(obj.items()):
                    result.append(" -- %s: %s" % (k, v))
            except Exception:
                result = res_dec
            playbook_path = os.path.join(
                os.path.basename(os.path.dirname(path)), os.path.basename(path)
            )
            self.lines.append(
                "PLAYBOOK [%s] TASK [%s]: %s\n"
                % (playbook_path, name.replace(" ", "_"), status)
            )
            for line in result:
                self.lines.append("%s\n" % (line))
            if stdout:
                self.lines.append(" -- STDOUT:\n")
                for line in stdout.split("\n"):
                    self.lines.append("%s\n" % line)
            if stderr:
                self.lines.append(" -- STDERR:\n")
                for line in stderr.split("\n"):
                    self.lines.append("%s\n" % line)
            self.lines.append("\n")
        c.close()
        con.close()

    def __str__(self):
        return "ARA Report %s" % self.db_path

    # Fake string interface
    def rfind(self, *args):
        return -1

    def startswith(self, *args):
        return False

    def __getitem__(self, *args):
        return self.db_path

    def close(self):
        pass


def json_dumps(report):
    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Journal):
                return "<Journal %s>" % o.name
            elif isinstance(o, AraReport):
                return "<ARA %s>" % o.db_path
            return json.JSONEncoder.default(self, o)

    return json.dumps(report, cls=JSONEncoder)


OpenedFile = Union[FileLike, BinaryIO, gzip.GzipFile, lzma.LZMAFile]


def open_file(p: LogObject) -> OpenedFile:
    if isinstance(p, FileLike):
        p.open()
        return p
    elif isinstance(p, dict):
        raise RuntimeError("Can't open a build!")
    elif p.endswith(".gz"):
        # check if really gzip, logs.openstack.org return decompressed files
        if open(p, "rb").read(2) == b"\x1f\x8b":
            return gzip.open(p, mode="r")
    elif p.endswith(".xz"):
        return lzma.open(p, mode="r")
    fobj = open(p, "rb")
    # Try to decode the first few byte to detect binary files
    fobj.peek(32).decode("utf-8")  # type: ignore
    return fobj


def files_iterator(
    paths: Sequence[LogObject],
    keep_file: Callable[[str], bool] = lambda s: True,
) -> Generator[Tuple[LogObject, str], None, None]:
    """Walk directory and yield (path, rel_path)"""
    # Copy path list
    paths = list(paths)
    for path in paths:
        if isinstance(path, dict):
            # This is a build object, return the log's local path
            path = path["local_path"]
        if isinstance(path, Journal):
            yield (path, "")
        elif not isinstance(path, str):
            raise RuntimeError("%s: unknown uri" % path)
        elif os.path.isfile(path):
            if path.endswith("ara-report/ansible.sqlite"):
                yield (AraReport(path), "report/ansible.sqlite")
            else:
                yield (path, os.path.basename(path))
        elif os.path.isdir(path):
            if path[-1] != "/":
                path = "%s/" % path
            for dname, _, fnames in os.walk(path):
                for fname in fnames:
                    fpath = os.path.join(dname, fname)
                    rel_path = fpath[len(path) :]
                    if not keep_file(rel_path):
                        continue

                    if fname != "ansible.sqlite" and [
                        True
                        for skip in BLACKLIST_EXTENSIONS
                        if fname.endswith("%s" % skip)
                        or fname.endswith("%s.gz" % skip)
                        or fname.endswith("%s.txt.gz" % skip)
                        or fname.endswith("%s.bz2" % skip)
                        or fname.endswith("%s.bzip2" % skip)
                        or fname.endswith("%s.xz" % skip)
                    ]:
                        continue

                    # Skip empty files
                    try:
                        zero_sizes = [0]
                        if ".gz" in fpath:
                            zero_sizes.append(20)
                        if os.stat(fpath).st_size in zero_sizes:
                            continue
                    except Exception:
                        pass

                    if fname == "ansible.sqlite":
                        yield (AraReport(fpath), "report/ansible.sqlite")
                    else:
                        yield (fpath, rel_path)
        else:
            raise RuntimeError("%s: unknown uri" % path)


def setup_logging(debug=False):
    loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG
    logging.basicConfig(
        format="%(asctime)s %(levelname)-5.5s %(name)s - %(message)s", level=loglevel
    )


def format_speed(count, size, elapsed_time):
    """Return speed in MB/s and kilo-line count/s"""
    # On windows, time.monotonic measurement seems to be of 15ms increment,
    # to prevent division by zero, pick the minimum value:
    elapsed_time = 0.015 if elapsed_time == 0 else elapsed_time
    return "%.03fs at %.03fMB/s (%0.3fkl/s) (%.03f MB - %.03f kilo-lines)" % (
        elapsed_time,
        (size / (1024 * 1024)) / elapsed_time,
        (count / 1000) / elapsed_time,
        (size / (1024 * 1024)),
        (count / 1000),
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        if os.path.basename(sys.argv[1]) == "ansible.sqlite":
            report = AraReport(sys.argv[1])
            for line in report.open():
                print(line[:-1].decode("utf-8"))
