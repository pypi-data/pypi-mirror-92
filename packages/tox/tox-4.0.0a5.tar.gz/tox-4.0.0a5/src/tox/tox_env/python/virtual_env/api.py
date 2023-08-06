"""
Declare the abstract base class for tox environments that handle the Python language via the virtualenv project.
"""
from abc import ABC
from pathlib import Path
from typing import Dict, List, Optional, Sequence, cast

from virtualenv import __version__ as virtualenv_version
from virtualenv import session_via_cli
from virtualenv.create.creator import Creator
from virtualenv.run.session import Session

from tox.config.cli.parser import DEFAULT_VERBOSITY, Parsed
from tox.config.loader.str_convert import StrConvert
from tox.config.sets import CoreConfigSet, EnvConfigSet
from tox.execute.api import Execute, Outcome, StdinSource
from tox.execute.local_sub_process import LocalSubProcessExecutor
from tox.journal import EnvJournal
from tox.report import ToxHandler
from tox.tox_env.errors import Recreate

from ..api import Python, PythonDeps, PythonInfo


class VirtualEnv(Python, ABC):
    """A python executor that uses the virtualenv project with pip"""

    def __init__(
        self, conf: EnvConfigSet, core: CoreConfigSet, options: Parsed, journal: EnvJournal, log_handler: ToxHandler
    ) -> None:
        self._virtualenv_session: Optional[Session] = None
        super().__init__(conf, core, options, journal, log_handler)

    def register_config(self) -> None:
        super().register_config()
        self.conf.add_config(
            keys=["system_site_packages", "sitepackages"],
            of_type=bool,
            default=lambda conf, name: StrConvert().to_bool(
                self.environment_variables.get("VIRTUALENV_SYSTEM_SITE_PACKAGES", "False")
            ),
            desc="create virtual environments that also have access to globally installed packages.",
        )
        self.conf.add_config(
            keys=["always_copy", "alwayscopy"],
            of_type=bool,
            default=lambda conf, name: StrConvert().to_bool(
                self.environment_variables.get(
                    "VIRTUALENV_COPIES", self.environment_variables.get("VIRTUALENV_ALWAYS_COPY", "False")
                )
            ),
            desc="force virtualenv to always copy rather than symlink",
        )
        self.conf.add_config(
            keys=["download"],
            of_type=bool,
            default=lambda conf, name: StrConvert().to_bool(
                self.environment_variables.get("VIRTUALENV_DOWNLOAD", "False")
            ),
            desc="true if you want virtualenv to upgrade pip/wheel/setuptools to the latest version",
        )

    def setup(self) -> None:
        with self._cache.compare({"version": virtualenv_version}, VirtualEnv.__name__) as (eq, old):
            if eq is False and old is not None:  # if changed create
                raise Recreate
        super().setup()

    def default_pass_env(self) -> List[str]:
        env = super().default_pass_env()
        env.append("PIP_*")  # we use pip as installer
        env.append("VIRTUALENV_*")  # we use virtualenv as isolation creator
        return env

    def default_set_env(self) -> Dict[str, str]:
        env = super().default_set_env()
        env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        return env

    def build_executor(self) -> Execute:
        return LocalSubProcessExecutor(self.options.is_colored)

    @property
    def session(self) -> Session:
        if self._virtualenv_session is None:
            env_dir = [str(cast(Path, self.conf["env_dir"]))]
            env = self.virtualenv_env_vars()
            self._virtualenv_session = session_via_cli(env_dir, options=None, setup_logging=False, env=env)
        return self._virtualenv_session

    def virtualenv_env_vars(self) -> Dict[str, str]:
        env = self.environment_variables.copy()
        base_python: List[str] = self.conf["base_python"]
        if "VIRTUALENV_CLEAR" not in env:
            env["VIRTUALENV_CLEAR"] = "True"
        if "VIRTUALENV_NO_PERIODIC_UPDATE" not in env:
            env["VIRTUALENV_NO_PERIODIC_UPDATE"] = "True"
        env["VIRTUALENV_SYSTEM_SITE_PACKAGES"] = str(self.conf["system_site_packages"])
        env["VIRTUALENV_COPIES"] = str(self.conf["always_copy"])
        env["VIRTUALENV_DOWNLOAD"] = str(self.conf["download"])
        env["VIRTUALENV_PYTHON"] = "\n".join(base_python)
        return env

    @property
    def creator(self) -> Creator:
        return self.session.creator

    def create_python_env(self) -> None:
        self.session.run()

    def _get_python(self, base_python: List[str]) -> Optional[PythonInfo]:
        try:
            interpreter = self.creator.interpreter
        except RuntimeError:  # if can't find
            return None
        return PythonInfo(
            executable=Path(interpreter.system_executable),
            implementation=interpreter.implementation,
            version_info=interpreter.version_info,
            version=interpreter.version,
            is_64=(interpreter.architecture == 64),
            platform=interpreter.platform,
            extra_version_info=None,
        )

    def python_env_paths(self) -> List[Path]:
        """Paths to add to the executable"""
        # we use the original executable as shims may be somewhere else
        return list(dict.fromkeys((self.creator.bin_dir, self.creator.script_dir)))

    def env_site_package_dir(self) -> Path:
        return cast(Path, self.creator.purelib)

    def env_python(self) -> Path:
        return cast(Path, self.creator.exe)

    def env_bin_dir(self) -> Path:
        return cast(Path, self.creator.script_dir)

    def install_python_packages(
        self,
        packages: PythonDeps,
        of_type: str,
        no_deps: bool = False,
        develop: bool = False,
        force_reinstall: bool = False,
    ) -> None:
        if not packages:
            return
        install_command = self.base_install_cmd
        if no_deps:
            install_command.append("--no-deps")
        if force_reinstall:
            install_command.append("--force-reinstall")
        if develop is True:
            install_command.extend(("--no-build-isolation", "-e"))
        install_command.extend(str(i) for i in packages)
        result = self.perform_install(install_command, f"install_{of_type}")
        result.assert_success()

    @property
    def base_install_cmd(self) -> List[str]:
        return [str(self.creator.exe), "-I", "-m", "pip", "install"]

    def perform_install(self, install_command: Sequence[str], run_id: str) -> Outcome:
        return self.execute(
            cmd=install_command,
            stdin=StdinSource.OFF,
            cwd=self.core["tox_root"],
            run_id=run_id,
            show=self.options.verbosity > DEFAULT_VERBOSITY,
        )

    def get_installed_packages(self) -> List[str]:
        list_command = [self.creator.exe, "-I", "-m", "pip", "freeze", "--all"]
        result = self.execute(
            cmd=list_command,
            stdin=StdinSource.OFF,
            run_id="freeze",
            show=self.options.verbosity > DEFAULT_VERBOSITY,
        )
        result.assert_success()
        return result.out.splitlines()
