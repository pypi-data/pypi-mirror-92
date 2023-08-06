# SPDX-License-Identifier: BSD-2-Clause
from unittest import mock
from pathlib import Path
import textwrap

import pytest
import marshmallow

import zsm_lib.config


def test_get_platform_path_returns_correct_path_on_freebsd():
    with mock.patch("platform.system", mock.MagicMock(return_value="FreeBSD")):
        path = zsm_lib.config.get_platform_path()

    assert path == Path("/usr/local/etc")


def test_get_platform_path_returns_correct_path_on_linux():
    with mock.patch("platform.system", mock.MagicMock(return_value="Linux")):
        path = zsm_lib.config.get_platform_path()

    assert path == Path("/etc")


def test_get_path():
    path = zsm_lib.config.get_path()
    assert path == zsm_lib.config.get_platform_path() / "zsm.yaml"


def test_schema_raises_validationerror_for_invalid_dataset_name(patch_zfs_get_datasets):
    data = {"snapshots": [{"dataset": "invalid/invalid"}]}

    with patch_zfs_get_datasets:
        with pytest.raises(marshmallow.ValidationError) as e:
            data = zsm_lib.config.ConfigSchema().load(data)

    assert "Dataset does not exist" in e.value.messages["snapshots"][0]["dataset"]


def test_load_works_with_valid_data(patch_zfs_get_datasets):
    data = """\
    snapshots:
      - dataset: "tank/a"
        label: "hourly"
        frequency: "1h"
        retention: 24
    """

    with patch_zfs_get_datasets:
        zsm_lib.config.load(data=textwrap.dedent(data))


def test_load_raises_validationerror_for_invalid_datas(patch_zfs_get_datasets):
    datas = [
        # Invalid YAML.
        "!@#",
        # Missing fields.
        """\
        snapshots:
          - dataset: "tank/a"
        """,
        # Label contains invalid character.
        """\
        snapshots:
          - dataset: "tank/a"
            label: "_"
            frequency: "1h"
            retention: 1
        """,
        # Frequency contains invalid unit.
        """\
        snapshots:
          - dataset: "tank/a"
            label: "a"
            frequency: "1p"
            retention: 1
        """,
    ]

    with patch_zfs_get_datasets:
        for data in datas:
            with pytest.raises(zsm_lib.config.ValidationError):
                zsm_lib.config.load(data=textwrap.dedent(data))
