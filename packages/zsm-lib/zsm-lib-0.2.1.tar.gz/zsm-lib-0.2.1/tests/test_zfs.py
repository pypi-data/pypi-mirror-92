# SPDX-License-Identifier: BSD-2-Clause
import pytest
from unittest import mock

import sarge

import zsm_lib.zfs


def get_mocked_readline(lines):
    if lines is None:
        lines = []

    # Always add an empty line to the end,
    # because that is how readline signals that there are no more lines.
    lines.append("")

    def generate_lines():
        for line in lines:
            yield line.encode("utf-8")

    generated_lines = generate_lines()

    def mocked_readline():
        return next(generated_lines)

    return mocked_readline


def test_run_with_success():
    mocked_pipeline = mock.MagicMock()
    mocked_pipeline.returncode = 0
    sarge.run = mock.MagicMock(return_value=mocked_pipeline)

    zsm_lib.zfs.run("asdf")

    sarge.run.assert_called()


def test_run_with_failure():
    expected_error = "a problem?"

    mocked_pipeline = mock.MagicMock()
    mocked_pipeline.returncode = 1
    mocked_pipeline.stderr.readline = get_mocked_readline([expected_error])
    sarge.run = mock.MagicMock(return_value=mocked_pipeline)

    with pytest.raises(zsm_lib.zfs.ZfsOperationFailed) as e:
        zsm_lib.zfs.run("asdf")

    assert str(e.value) == expected_error

    sarge.run.assert_called()


def patch_run(stdout_lines=None, stderr_lines=None):
    def mocked_run(cmd):
        mocked_stdout_capture = mock.MagicMock()
        mocked_stdout_capture.readline = get_mocked_readline(stdout_lines)

        mocked_stderr_capture = mock.MagicMock()
        mocked_stderr_capture.readline = get_mocked_readline(stderr_lines)

        mocked_pipeline = mock.MagicMock()
        mocked_pipeline.stdout = mocked_stdout_capture
        mocked_pipeline.stderr = mocked_stderr_capture

        return mocked_pipeline

    return mock.patch("zsm_lib.zfs.run", side_effect=mocked_run)


def test_get_datasets():
    stdout_lines = ["HEADER", "tank/a", "tank/b"]

    with patch_run(stdout_lines=stdout_lines):
        datasets = zsm_lib.zfs.get_datasets()

        # Start counting stdout_lines at 1 since the header is supposed to be skipped.
        assert datasets[0].name == stdout_lines[1]
        assert datasets[1].name == stdout_lines[2]


def test_get_snapshots():
    dataset_name = "tank/a"
    stdout_lines = ["HEADER", f"{dataset_name}@a", f"{dataset_name}@b"]

    with patch_run(stdout_lines=stdout_lines):

        snapshots = zsm_lib.zfs.get_snapshots(
            dataset=zsm_lib.zfs.Dataset(name="tank/a")
        )

        # Start counting stdout_lines at 1 since the header is supposed to be skipped.
        assert f"{dataset_name}@{snapshots[0].name}" == stdout_lines[1]
        assert f"{dataset_name}@{snapshots[1].name}" == stdout_lines[2]


def test_create_snapshot():
    with patch_run() as mock_run:
        zsm_lib.zfs.create_snapshot(
            dataset=zsm_lib.zfs.Dataset(name="tank/a"), name="asdf"
        )
        mock_run.assert_called()


def test_destroy_snapshot():
    with patch_run() as mock_run:
        zsm_lib.zfs.destroy_snapshot(
            snapshot=zsm_lib.zfs.Snapshot(
                dataset=zsm_lib.zfs.Dataset(name="tank/a"), name="asdf"
            )
        )
        mock_run.assert_called()
