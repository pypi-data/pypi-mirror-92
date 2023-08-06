# SPDX-License-Identifier: BSD-2-Clause
from unittest import mock

import pytest

import zsm_lib.zfs


@pytest.fixture(scope="function")
def patch_zfs_get_datasets():
    return mock.patch(
        "zsm_lib.zfs.get_datasets",
        return_value=[
            zsm_lib.zfs.Dataset(name="tank/a"),
            zsm_lib.zfs.Dataset(name="tank/b"),
            zsm_lib.zfs.Dataset(name="tank/c"),
        ],
    )
