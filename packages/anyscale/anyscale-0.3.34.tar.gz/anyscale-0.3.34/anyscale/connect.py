import os
import subprocess
from typing import Any, List, Optional, Union

import ray
import yaml

from anyscale.credentials import load_credentials
import anyscale.project
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK  # type: ignore

# The default project directory to use, if no project is specified.
DEFAULT_SCRATCH_DIR = "~/anyscale-connect-scratch"


class SessionBuilder:
    """This class lets you set session options and connect to Anyscale.

    This feature is ***EXPERIMENTAL***.

    It should not be constructed directly, but instead via anyscale.* methods
    exported at the package level.

    Examples:
        >>> # Raw client, creates new session on behalf of user
        >>> anyscale.connect()

        >>> # Get or create a named session
        >>> anyscale
        ...   .session("my_named_session")
        ...   .connect()

        >>> # Specify a previously created env / app template
        >>> anyscale
        ...   .app_env("prev_created_env:v2")
        ...   .autosuspend(hours=2)
        ...   .connect()

        >>> # Create new session from local env / from scratch
        >>> anyscale
        ...   .project_dir("~/dev/my-project-folder")
        ...   .base_docker_image("anyscale/ray-ml:latest")
        ...   .require("~/dev/my-project-folder/requirements.txt")
        ...   .connect()

        >>> # Ray client connect is setup automatically
        >>> @ray.remote
        ... def my_func(value):
        ...   return value ** 2

        >>> # Remote functions are executed in the Anyscale session
        >>> print(ray.get([my_func.remote(x) for x in range(5)]))
        >>> [0, 1, 4, 9, 16]
    """

    def __init__(
        self,
        scratch_dir: str = DEFAULT_SCRATCH_DIR,
        anyscale_sdk: AnyscaleSDK = None,
        subprocess: Any = subprocess,
        ray: Any = ray,
    ) -> None:
        self._anyscale_sdk: Any = None
        if anyscale_sdk:
            self._anyscale_sdk = anyscale_sdk
        else:
            self._anyscale_sdk = AnyscaleSDK(load_credentials())
        self._ray: Any = ray
        self._subprocess: Any = subprocess
        self._scratch_dir: str = scratch_dir
        self._project_dir: Optional[str] = None
        self._session_name: str = "session-1"
        self._connected: bool = False

    def connect(self) -> None:
        """Connect to Anyscale using previously specified options.

        Examples:
            >>> anyscale.connect()
        """

        assert not self._connected, "Cannot call connect() twice."

        # Autodetect or create a scratch project.
        if self._project_dir is None:
            self._project_dir = anyscale.project.find_project_root(os.getcwd())
        if self._project_dir:
            self._ensure_project_setup_at_dir(self._project_dir)
        else:
            self._project_dir = self._get_or_create_scratch_project()
        proj_def = anyscale.project.ProjectDefinition(self._project_dir)
        project_id = anyscale.project.get_project_id(proj_def.root)
        print("Using project dir", proj_def.root)

        # TODO(ekl): generate a serverless compute configuraton here.
        cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)
        cluster_yaml["setup_commands"] = [
            "pip install -U https://s3-us-west-2.amazonaws.com/ray-wheels/"
            "latest/ray-1.2.0.dev0-cp37-cp37m-manylinux2014_x86_64.whl"
        ]
        cluster_yaml["head_start_ray_commands"] = [
            "ray stop",
            "ulimit -n 65536; ray start --head --port=6379 "
            "--object-manager-port=8076 "
            "--ray-client-server-port=10001 "
            "--autoscaling-config=~/ray_bootstrap_config.yaml",
        ]

        with open(os.path.join(self._project_dir, "session-default.yaml"), "w+") as f:
            f.write(yaml.dump(cluster_yaml))

        # TODO(ekl): better logging here
        self._subprocess.check_call(
            [
                "anyscale",
                "up",
                "--cloud-name",
                "anyscale_default_cloud",
                self._session_name,
            ],
            cwd=self._project_dir,
        )

        query = self._anyscale_sdk.search_sessions(project_id=project_id)
        session_found = None
        for session in query.results:
            if session.name == self._session_name:
                session_found = session
                break
        if not session_found:
            raise RuntimeError(
                "Failed to locate session: {}".format(self._session_name)
            )

        full_url = session_found.service_proxy_url
        # like "session-fqsx0p3pzfna71xxxxxxx.anyscaleuserdata.com:8081"
        session_url = full_url.split("/")[2].lower() + ":8081"
        # like "8218b528-7363-4d04-8358-57936cdxxxxx"
        auth_token = full_url.split("?token=")[1].split("&")[0]

        metadata = [("cookie", "anyscale-token=" + auth_token), ("port", "10001")]
        print("Connecting to Ray", session_url, metadata)
        self._ray.util.connect(session_url, secure=False, metadata=metadata)
        print("Checking connection...")

        def func() -> str:
            return "Connected!"

        f_remote = self._ray.remote(func)

        print(self._ray.get(f_remote.remote()))
        self._connected = True

    def project_dir(self, local_dir: str) -> "SessionBuilder":
        """Set the project directory.

        This sets the project code directory that will be synced to all nodes
        in the cluster as required by Ray. If not specified, the project
        directory will be autodetected based on the current working directory.
        If no Anyscale project is found, a "scratch" project will be used.

        Args:
            local_dir (str): path to the project directory.

        Examples:
            >>> anyscale.project_dir("~/my-proj-dir").connect()
        """
        self._project_dir = os.path.abspath(os.path.expanduser(local_dir))
        return self

    def session(self, session_name: str, update: bool = True) -> "SessionBuilder":
        """Set a fixed session name.

        By default, Anyscale connect will pick an idle session compatible
        with the connect parameters, creating a new session if no compatible
        idle sessions. Setting a fixed session name will force connecting to
        the given named session, creating it if it doesn't exist.

        Args:
            session_name (str): fixed name of the session.
            update (bool): whether to update session configurations when
                connecting to an existing session. Note that this may restart
                the Ray runtime.

        Examples:
            >>> anyscale.session("prod_deployment", update=True).connect()
        """
        if not update:
            raise NotImplementedError("TODO implement no update connect")
        self._session_name = session_name
        return self

    def base_docker_image(self, image_name: str) -> "SessionBuilder":
        """Set the docker image to use for the session.

        Args:
            image_name (str): docker image name.

        Examples:
            >>> anyscale.base_docker_image("anyscale/ray-ml:latest").connect()
        """
        raise NotImplementedError()

    def require(self, requirements: Union[str, List[str]]) -> "SessionBuilder":
        """Set the Python requirements for the session.

        Args:
            requirements: either be a list of pip library specifications, or
            the path to a requirements.txt file.

        Examples:
            >>> anyscale.require("~/proj/requirements.txt").connect()
            >>> anyscale.require(["gym", "torch>=1.4.0"]).connect()
        """
        raise NotImplementedError()

    def app_env(self, env_name: str) -> "SessionBuilder":
        """Set the Anyscale app env to use for the session.

        Args:
            env_name (str): app env name.

        Examples:
            >>> anyscale.app_env("prev_created_env:v2").connect()
        """
        raise NotImplementedError()

    def file_mount(self, *, local_dir: str, remote_dir: str) -> "SessionBuilder":
        """Add additional directories to sync up to worker nodes.

        Args:
            local_dir (str): the local directory path to mount.
            remote_dir (str): where in the remote node to mount the local dir.

        Examples:
            >>> anyscale
            ...   .file_mount(local_dir="~/data1", remote_dir="/tmp/d1")
            ...   .file_mount(local_dir="~/data2", remote_dir="/tmp/d2")
            ...   .connect()
        """
        raise NotImplementedError()

    def download_results(
        self, *, remote_dir: str, local_dir: str, autosync: bool = False
    ) -> "SessionBuilder":
        """Specify a directory to sync down from the cluster head node.

        Args:
            remote_dir (str): the remote result dir on the head node.
            local_dir (str): the local path to sync results to.
            autosync (bool): whether to sync the files continuously. By
                default, results will only be synced on job completion.

        Examples:
            >>> anyscale
            ...   .download_results(
            ...       remote_dir="~/ray_results", remote_dir="~/proj_output",
            ...       autosync=True)
            ...   .connect()
        """
        raise NotImplementedError()

    def autoshutdown(
        self, enabled: bool = True, *, hours: int = 1, minutes: int = 0,
    ) -> "SessionBuilder":
        """Configure or disable session autoshutdown behavior.

        The session will be autoshutdown after the specified time period. By
        default, sessions auto terminate after one hour of idle.

        Args:
            enabled (bool): whether autoshutdown is enabled.
            hours (int): specify idle time in hours.
            minutes (int): specify idle time in minutes. This is added to the
                idle time in hours.

        Examples:
            >>> anyscale.autoshutdown(False).connect()
            >>> anyscale.autoshutdown(hours=10).connect()
            >>> anyscale.autoshutdown(hours=1, minutes=30).connect()
        """
        raise NotImplementedError()

    def _get_or_create_scratch_project(self) -> str:
        """Get or create a scratch project, including the directory."""
        project_dir = os.path.expanduser(self._scratch_dir)
        self._ensure_project_setup_at_dir(project_dir)
        return project_dir

    def _ensure_project_setup_at_dir(self, project_dir: str) -> None:
        """Get or create an Anyscale project rooted at the given dir."""
        os.makedirs(project_dir, exist_ok=True)
        proj_name = os.path.basename(project_dir)

        # If the project yaml exists, assume we're already setup.
        project_yaml = os.path.join(project_dir, ".anyscale.yaml")
        if os.path.exists(project_yaml):
            return

        print("Creating new project for", project_dir)
        project_response = self._anyscale_sdk.create_project(
            {
                "name": proj_name,
                "description": "Automatically created by Anyscale Connect",
            }
        )
        project_id = project_response.result.id

        if not os.path.exists(project_yaml):
            with open(project_yaml, "w+") as f:
                f.write(yaml.dump({"project_id": project_id}))
