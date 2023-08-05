#!/bin/env python3
#
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

import argparse
import json
import logging
import os
import time
import yaml

import logreduce.download
import logreduce.utils

from typing import List, Optional, Sequence
from logreduce.data import Build, LogObject, show_build
from logreduce.process import Classifier
from logreduce.html_output import render_html
from logreduce.models import models
from logreduce.utils import keep_file, process_line


DEFAULT_ZUUL_WEB = os.environ.get(
    "ZUUL_WEB", "https://softwarefactory-project.io/zuul/api/tenant/local"
)


class Cli:
    log = logging.getLogger("LogReduce")

    def __init__(self) -> None:
        self.job = "unknown-job"
        self.exclude_file = logreduce.utils.DEFAULT_IGNORE_FILES
        self.exclude_path = logreduce.utils.DEFAULT_IGNORE_PATHS
        self.exclude_line: List[str] = []
        self.test_prefix = None
        self.ara_database = False
        self.context_length = None
        self.json = None
        self.html = None
        self.threshold = 0.2
        self.merge_distance = 5
        self.before_context = 3
        self.after_context = 1
        self.max_age = 7
        self.range = "week"
        self.static_location = None
        self.pipeline = None
        self.branch = None
        self.project = None
        self.count = None
        self.tmp_dir = os.getcwd()
        self.model_type = None
        self.cacheonly = False

        # Parse args
        parser = self.usage()
        args = parser.parse_args()
        if not args.func:
            parser.print_help()
            exit(4)
        logreduce.utils.setup_logging(args.debug)
        kwargs = {}
        for k, v in args.__dict__.items():
            if k == "exclude_file":
                self.exclude_file.extend(v)
            elif k == "exclude_path":
                self.exclude_path.extend(v)
            elif k == "exclude_line":
                self.exclude_line.extend(v)
            elif k in ("logs_url", "model_file", "target", "baseline", "target_dir"):
                # function argument
                kwargs[k] = v
            else:
                # class member variables
                self.__dict__[k] = v

        # Add config default
        config = yaml.safe_load(open(args.config)) if args.config else {}
        for k in ("exclude_lines", "exclude_files", "exclude_paths"):
            if config.get("filters", {}).get(k):
                # class attribute are singular, without the 's'
                attribute = k[:-1]
                getattr(self, attribute).extend(config["filters"][k])

        # Convenient trick
        if "logs.openstack.org" in kwargs.get("logs_url", ""):
            self.zuul_web = "http://zuul.openstack.org/api"
        if "logs.rdoproject.org" in kwargs.get("logs_url", ""):
            self.zuul_web = (
                "https://softwarefactory-project.io/zuul/api/" "tenant/rdoproject.org"
            )

        # Remove ara-report exclude
        if self.ara_database:
            try:
                self.exclude_path.remove("ara[_-]*.*/")
            except ValueError:
                pass

        try:
            args.func(**kwargs)
        except RuntimeError as e:
            print(e)
            exit(4)

    def usage(self):
        parser = argparse.ArgumentParser()
        parser.set_defaults(func=None)
        parser.add_argument("--config", help="Config file for defaults filters")
        parser.add_argument("--debug", action="store_true", help="Print debug")
        parser.add_argument("--tmp-dir", default=self.tmp_dir)
        parser.add_argument(
            "--cacheonly", action="store_true", help="Do not download any logs"
        )
        parser.add_argument(
            "--model-type",
            default="hashing_nn",
            choices=list(models.keys()),
            help="The model type",
        )

        # Common arguments
        def path_filters(s):
            s.add_argument(
                "-x",
                "--exclude-file",
                action="append",
                default=[],
                help="Filename (basename) exclude regexp",
            )
            s.add_argument(
                "-X",
                "--exclude-path",
                action="append",
                default=[],
                help="Path exclude regexp",
            )
            s.add_argument(
                "-f",
                "--exclude-line",
                action="append",
                default=[],
                help="Log line exclude regexp",
            )
            s.add_argument(
                "--test-prefix",
                help="Local path mapping to logserver directory. "
                "(e.g.: 'controller/logs' for '/opt/stack/logs')",
            )

        def job_filters(s):
            s.add_argument("--job", help="The job name")
            s.add_argument(
                "--branch", default="master", help="The branch name [%(default)s]"
            )
            s.add_argument(
                "--pipeline",
                help="The pipeline to fetch baseline from, " "e.g. gate or periodic",
            )
            s.add_argument("--project", help="Build a model per project")
            s.add_argument(
                "--zuul-web",
                default=DEFAULT_ZUUL_WEB,
                help="The zuul-web url (including the tenant name)" " [%(default)s]",
            )
            s.add_argument(
                "--count",
                type=int,
                default=1,
                help="The number of baseline to use [%(default)s]",
            )

        def report_filters(s):
            s.add_argument("--html", metavar="FILE", help="Render html result")
            s.add_argument("--json", metavar="FILE", help="Optional json output")
            s.add_argument(
                "-d", "--static-location", help="The js/css static directory location"
            )
            s.add_argument(
                "-t",
                "--threshold",
                default=self.threshold,
                type=float,
                help="Anomalies distance threshold [%(default)s]",
            )
            s.add_argument(
                "-M",
                "--merge-distance",
                default=self.merge_distance,
                type=int,
                help="Distance between chunks to merge in a continuous one"
                " [%(default)s]",
            )
            s.add_argument(
                "-B",
                "--before-context",
                default=self.before_context,
                type=int,
                help="Amount of lines to include before the anomaly" " [%(default)s]",
            )
            s.add_argument(
                "-A",
                "--after-context",
                default=self.after_context,
                type=int,
                help="Amount of lines to include after the anomaly" " [%(default)s]",
            )
            s.add_argument(
                "-C",
                "--context-length",
                type=int,
                help="Set both before and after context size",
            )

        def model_filters(s):
            s.add_argument(
                "-m",
                "--max-age",
                type=int,
                default=self.max_age,
                help="Maximum age of a model [%(default)s]",
            )

        def journal_filters(s):
            s.add_argument(
                "-r",
                "--range",
                choices=("day", "week", "month"),
                default=self.range,
                help="Training/testing time frame range " " [%(default)s]",
            )

        # Sub command usages
        def model_check_usage(sub):
            s = sub.add_parser("model-check", help="Check if a model is valid")
            s.set_defaults(func=self.model_check)
            model_filters(s)
            s.add_argument("model_file")

        def model_run_usage(sub):
            s = sub.add_parser("model-run", help="Run a model")
            s.set_defaults(func=self.model_run)
            path_filters(s)
            report_filters(s)
            s.add_argument("model_file")
            s.add_argument("target", nargs="+")

        # Local directory
        def dir_train_usage(sub):
            s = sub.add_parser("dir-train", help="Build a model for local files/dirs")
            s.set_defaults(func=self.dir_train)
            model_filters(s)
            path_filters(s)
            s.add_argument("model_file")
            s.add_argument("baseline", nargs="+")

        def dir_run_usage(sub):
            s = sub.add_parser("dir-run", help="Run a model against local files/dirs")
            s.set_defaults(func=self.dir_run)
            report_filters(s)
            path_filters(s)
            s.add_argument("model_file")
            s.add_argument("target")

        def dir_usage(sub):
            s = sub.add_parser("dir", help="Train and run against local files/dirs")
            s.set_defaults(func=self.dir_allinone)
            model_filters(s)
            report_filters(s)
            path_filters(s)
            s.add_argument("baseline")
            s.add_argument("target")

        # Zuul integration
        def job_train_usage(sub):
            s = sub.add_parser("job-train", help="Build a model for a CI job")
            s.add_argument(
                "--ara-database", action="store_true", help="Train on ara database"
            )
            s.set_defaults(func=self.job_train)
            model_filters(s)
            job_filters(s)
            path_filters(s)
            s.add_argument("model_file")

        def job_run_usage(sub):
            s = sub.add_parser("job-run", help="Run a model against CI logs")
            s.set_defaults(func=self.job_run)
            report_filters(s)
            s.add_argument(
                "--zuul-web",
                default=DEFAULT_ZUUL_WEB,
                help="The zuul-web url (including the tenant name)" " [%(default)s]",
            )
            path_filters(s)
            s.add_argument("model_file")
            s.add_argument("logs_url", help="The CI logs url or a local dir")

        def job_usage(sub):
            s = sub.add_parser("job", help="Train and run against CI logs")
            s.set_defaults(func=self.job_allinone)
            model_filters(s)
            report_filters(s)
            job_filters(s)
            path_filters(s)
            s.add_argument("logs_url")

        # Journald integration
        def journal_train_usage(sub):
            s = sub.add_parser("journal-train", help="Build a model for local journald")
            s.set_defaults(func=self.journal_train)
            journal_filters(s)
            model_filters(s)
            s.add_argument("model_file")

        def journal_run_usage(sub):
            s = sub.add_parser(
                "journal-run", help="Run a model against a local journald"
            )
            s.set_defaults(func=self.journal_run)
            journal_filters(s)
            report_filters(s)
            s.add_argument("model_file")

        def journal_usage(sub):
            s = sub.add_parser("journal", help="Train and run against local journald")
            s.set_defaults(func=self.journal_allinone)
            journal_filters(s)
            report_filters(s)

        # Extra command line usage...
        def download_logs_usage(sub):
            s = sub.add_parser("download-logs", help="Get the logs")
            s.set_defaults(func=self.download_logs)
            path_filters(s)
            s.add_argument("logs_url", help="The logs file url")
            s.add_argument("target_dir", nargs="?")

        def diff_usage(sub):
            s = sub.add_parser("diff", help="Compare directories/files")
            s.set_defaults(func=self.diff)
            report_filters(s)
            s.add_argument("baseline", nargs="+")
            s.add_argument("target")

        sub_parser = parser.add_subparsers()
        model_check_usage(sub_parser)
        model_run_usage(sub_parser)
        dir_train_usage(sub_parser)
        dir_run_usage(sub_parser)
        dir_usage(sub_parser)
        job_train_usage(sub_parser)
        job_run_usage(sub_parser)
        job_usage(sub_parser)
        journal_train_usage(sub_parser)
        journal_run_usage(sub_parser)
        journal_usage(sub_parser)
        download_logs_usage(sub_parser)
        diff_usage(sub_parser)
        return parser

    def model_check(self, model_file: str) -> None:
        max_age_sec = self.max_age * 24 * 3600
        if (
            not os.path.exists(model_file)
            or time.time() - os.stat(model_file).st_mtime > max_age_sec
        ):
            raise RuntimeError("%s: does not exists or too old" % model_file)
        try:
            Classifier.check(open(model_file, "rb"))
        except Exception as e:
            raise RuntimeError("%s: %s" % (model_file, e))

    def model_run(self, model_file: str, targets: Sequence[LogObject]) -> None:
        clf = self._get_classifier(model_file)
        self._report(clf, targets)

    # Local file usage
    def dir_train(self, model_file: str, baseline: List[str]) -> Classifier:
        clf = self._get_classifier()
        clf.train(baseline)
        clf.save_file(model_file)
        return clf

    def dir_run(self, model_file: str, target: str) -> None:
        clf = self._get_classifier(model_file)
        self._report(clf, target)

    def dir_allinone(self, baseline: str, target: str) -> None:
        model_file = os.path.join(
            self.tmp_dir, "_models", baseline.replace("/", "_") + ".clf"
        )
        clf = None
        if os.path.exists(model_file):
            try:
                clf = self._get_classifier(model_file)
            except Exception:
                self.log.exception("Couldn't reuse %s" % model_file)
        if clf is None:
            clf = self.dir_train(model_file, [baseline])
        self._report(clf, target)

    # Zuul job usage
    def job_train(self, model_file: str) -> Classifier:
        # Discover baseline
        baselines: List[Build] = []
        if self.pipeline:
            pipelines = [self.pipeline]
        else:
            pipelines = ["periodic", "gate", "check"]
        for pipeline in pipelines:
            for baseline in logreduce.download.ZuulBuilds(self.zuul_web).get(
                job=self.job,
                result="SUCCESS",
                branch=self.branch,
                pipeline=pipeline,
                project=self.project,
                count=self.count,
            ):
                baselines.append(baseline)
            if baselines:
                break
        if not baselines:
            print(
                "%s: couldn't find success in pipeline %s"
                % (self.job, " ".join(pipelines))
            )
            exit(4)
        for baseline in baselines:
            if baseline["log_url"][-1] != "/":
                baseline["log_url"] += "/"
            dest = os.path.join(
                self.tmp_dir, "_baselines", self.job, baseline["log_url"].split("/")[-2]
            )
            self.download_logs(baseline["log_url"], dest)
            baseline["local_path"] = dest

        # Train model
        clf = self._get_classifier()
        clf.train(baselines)
        clf.save_file(model_file)
        print("%s: built with %s" % (model_file, " ".join(map(show_build, baselines))))
        return clf

    def job_run(self, model_file: str, logs_url: str) -> None:
        clf = self._get_classifier(model_file)
        if os.path.exists(logs_url):
            target = logs_url
        else:
            target = self.download_logs(logs_url)
        build = self._get_build(target)
        if build:
            self._report(clf, [build])

    def job_allinone(self, logs_url: str) -> None:
        if self.job is None:
            self.job = logs_url.split("/")[-3]
        model_name = self.job + ".clf"
        if self.project is not None:
            model_name = os.path.join(self.project, model_name)
        model_file = os.path.join(self.tmp_dir, "_models", model_name)
        clf = None
        if os.path.exists(model_file):
            try:
                clf = self._get_classifier(model_file)
            except Exception:
                self.log.exception("Couldn't reuse %s" % model_file)
        if clf is None:
            clf = self.job_train(model_file)

        target = self.download_logs(logs_url)
        build = self._get_build(target)
        if build:
            self._report(clf, [build])

    def _get_build(self, target: str) -> Optional[Build]:
        build_cache = os.path.join(target, "zuul-info/build.json")
        if os.path.exists(build_cache):
            return json.load(open(build_cache))
        inv_path = os.path.join(target, "zuul-info/inventory.yaml")
        try:
            inv = yaml.safe_load(open(inv_path))
        except FileNotFoundError:
            self.log.info("%s: couldn't find file", inv_path)
            return None
        try:
            build_uuid = inv["all"]["vars"]["zuul"]["build"]
        except KeyError:
            self.log.info("%s: couldn't find build id", inv_path)
            return None
        try:
            build = logreduce.download.ZuulBuilds(self.zuul_web).get(uuid=build_uuid)[0]
        except IndexError:
            self.log.warning("%s: couldn't find build", build_uuid)
            return None
        build["local_path"] = target
        json.dump(build, open(build_cache, "w"))
        return build

    # Jounrald usage
    def journal_train(self, model_file: str) -> Classifier:
        baseline = logreduce.utils.Journal(self.range, previous=True)
        clf = self._get_classifier()
        clf.train([baseline])
        clf.save_file(model_file)
        return clf

    def journal_run(self, model_file: str) -> None:
        clf = self._get_classifier(model_file)
        target = logreduce.utils.Journal(self.range)
        self._report(clf, [target])

    def journal_allinone(self) -> None:
        model_file = os.path.join(
            self.tmp_dir, "_models", "jounral-%s.clf" % self.range
        )
        clf = None
        if os.path.exists(model_file):
            try:
                clf = self._get_classifier(model_file)
            except Exception:
                self.log.exception("Couldn't reuse %s" % model_file)
        if clf is None:
            clf = self.journal_train(model_file)
        target = logreduce.utils.Journal(self.range)
        self._report(clf, [target])

    def diff(self, baseline: str, target: str) -> None:
        clf = self._get_classifier()
        clf.train(baseline)
        self._report(clf, target)

    def download_logs(self, logs_url: str, target_dir=None) -> str:
        if logs_url.endswith("/job-output.txt.gz"):
            logs_url = logs_url[: -len("/job-output.txt.gz")]
        if logs_url[-1] != "/":
            logs_url += "/"
        if target_dir is None:
            if self.job is None:
                self.job = logs_url.split("/")[-3]
            target_dir = os.path.join(
                self.tmp_dir, "_targets", self.job, logs_url.split("/")[-2]
            )
        if self.cacheonly:
            return target_dir

        os.makedirs(target_dir, exist_ok=True)

        logreduce.download.RecursiveDownload(
            logs_url,
            target_dir,
            trim=logs_url,
            exclude_files=self.exclude_file,
            exclude_paths=self.exclude_path,
            exclude_extensions=logreduce.utils.BLACKLIST_EXTENSIONS,
        ).wait()
        return target_dir

    def _get_classifier(self, model_file: str = None) -> Classifier:
        if model_file is not None:
            clf = Classifier.load_file(
                model_file,
                keep_file=keep_file(self.exclude_file, self.exclude_path),
                process_line=process_line(self.exclude_line),
            )
        else:
            clf = Classifier(
                self.model_type,
                keep_file=keep_file(self.exclude_file, self.exclude_path),
                process_line=process_line(self.exclude_line),
            )
        clf.test_prefix = self.test_prefix
        return clf

    def _report(
        self,
        clf: Classifier,
        target_dirs: Sequence[LogObject],
        target_source: Optional[str] = None,
    ) -> None:
        if self.context_length is not None:
            self.before_context = self.context_length
            self.after_context = self.context_length

        console_output = True
        if self.json or self.html:
            console_output = False
        output = clf.process(
            path=target_dirs,
            path_source=target_source,
            threshold=float(self.threshold),
            merge_distance=self.merge_distance,
            before_context=self.before_context,
            after_context=self.after_context,
            console_output=console_output,
        )
        if not output.get("anomalies_count"):
            exit(4)
        if self.html:
            open(self.html, "w").write(render_html(output, self.static_location))
            open(self.html.replace(".html", ".json"), "w").write(
                logreduce.utils.json_dumps(output)
            )
        if self.json:
            open(self.json, "w").write(logreduce.utils.json_dumps(output))
        else:
            print(
                "%02.2f%% reduction (from %d lines to %d)"
                % (
                    output["reduction"],
                    output["testing_lines_count"],
                    output["outlier_lines_count"],
                )
            )


def main():
    try:
        Cli()
    except RuntimeError as e:
        print(e)
        exit(4)


if __name__ == "__main__":
    main()
