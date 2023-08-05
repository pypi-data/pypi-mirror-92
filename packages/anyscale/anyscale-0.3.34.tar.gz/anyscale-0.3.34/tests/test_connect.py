from datetime import datetime
import os
from pathlib import Path
from typing import Any, Tuple
from unittest.mock import Mock

import yaml

import anyscale
from anyscale.client.openapi_client.models.project import Project  # type: ignore
from anyscale.client.openapi_client.models.project_response import ProjectResponse  # type: ignore
from anyscale.client.openapi_client.models.session import Session  # type: ignore
from anyscale.connect import SessionBuilder

UP_CMD = ["anyscale", "up"]


def _make_test_builder(tmp_path: Path) -> Tuple[Any, Any, Any, Any]:
    scratch = tmp_path / "scratch"
    sdk = Mock()
    sess_resp = Mock()
    ray = Mock()
    sess_resp.results = [
        Session(
            id="session_id",
            name="session-1",
            created_at=datetime.now(),
            snapshots_history=[],
            idle_timeout=120,
            tensorboard_available=False,
            project_id="project_id",
            state="Running",
            service_proxy_url="http://session-foo.userdata.com/auth?token=value&bar",
            last_activity_at=datetime.now(),
        )
    ]
    sdk.search_sessions.return_value = sess_resp
    subprocess = Mock()
    builder = SessionBuilder(
        scratch_dir=scratch.absolute().as_posix(),
        anyscale_sdk=sdk,
        subprocess=subprocess,
        ray=ray,
    )
    return builder, sdk, subprocess, ray


def test_new_proj_connect_params(tmp_path: Path, project_test_data: Project) -> None:
    project_dir = (tmp_path / "my_proj").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file
    builder.project_dir(project_dir).connect()

    assert anyscale.project.get_project_id(project_dir)
    subprocess.check_call.assert_called_once_with(
        UP_CMD + ["--cloud-name", "anyscale_default_cloud", "session-1"],
        cwd=project_dir,
    )

    # Also check connection params in this test.
    ray.util.connect.assert_called_once_with(
        "session-foo.userdata.com:8081",
        metadata=[("cookie", "anyscale-token=value"), ("port", "10001")],
        secure=False,
    )


def test_detect_existing_proj(tmp_path: Path) -> None:
    nested_dir = (tmp_path / "my_proj" / "nested").absolute().as_posix()
    parent_dir = os.path.dirname(nested_dir)
    os.makedirs(nested_dir)
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)

    # Setup project in parent dir
    project_yaml = os.path.join(parent_dir, ".anyscale.yaml")
    with open(project_yaml, "w+") as f:
        f.write(yaml.dump({"project_id": 12345}))

    # Should detect the parent project dir
    cwd = os.getcwd()
    try:
        os.chdir(nested_dir)
        builder.connect()
    finally:
        os.chdir(cwd)

    subprocess.check_call.assert_called_once_with(
        UP_CMD + ["--cloud-name", "anyscale_default_cloud", "session-1"],
        cwd=parent_dir,
    )


def test_fallback_scratch_dir(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.connect()

    assert anyscale.project.get_project_id(scratch_dir)
    subprocess.check_call.assert_called_once_with(
        UP_CMD + ["--cloud-name", "anyscale_default_cloud", "session-1"],
        cwd=scratch_dir,
    )
