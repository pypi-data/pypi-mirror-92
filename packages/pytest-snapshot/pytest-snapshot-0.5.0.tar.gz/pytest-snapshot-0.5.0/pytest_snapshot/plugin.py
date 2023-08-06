import os
import re

import pytest
import _pytest.python
from packaging import version
from typing import List, Dict, Union

from pathlib import Path

PARAMETRIZED_TEST_REGEX = re.compile(r'^.*?\[(.*)]$')


def pytest_addoption(parser):
    group = parser.getgroup('snapshot')
    group.addoption(
        '--snapshot-update',
        action='store_true',
        help='Update snapshots.'
    )
    group.addoption(
        '--allow-snapshot-deletion',
        action='store_true',
        help='Allow snapshot deletion when updating snapshots.'
    )


@pytest.fixture
def snapshot(request):
    default_snapshot_dir = get_default_snapshot_dir(request.node)

    with Snapshot(request.config.option.snapshot_update,
                  request.config.option.allow_snapshot_deletion,
                  default_snapshot_dir) as snapshot:
        yield snapshot


class Snapshot(object):
    _snapshot_update = None  # type: bool
    _allow_snapshot_deletion = None  # type: bool
    _created_snapshots = None  # type: List[Path]
    _updated_snapshots = None  # type: List[Path]
    _snapshots_to_delete = None  # type: List[Path]
    _snapshot_dir = None  # type: Path

    def __init__(self, snapshot_update: bool, allow_snapshot_deletion: bool, snapshot_dir: Path):
        self._snapshot_update = snapshot_update
        self._allow_snapshot_deletion = allow_snapshot_deletion
        self._created_snapshots = []
        self._updated_snapshots = []
        self._snapshots_to_delete = []
        self.snapshot_dir = snapshot_dir

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._created_snapshots or self._updated_snapshots or self._snapshots_to_delete:
            message_lines = ['Snapshot directory was modified: {}'.format(shorten_path(self.snapshot_dir))]
            if self._created_snapshots:
                message_lines.append('  Created snapshots:')
                message_lines.extend('    ' + str(s.relative_to(self.snapshot_dir)) for s in self._created_snapshots)

            if self._updated_snapshots:
                message_lines.append('  Updated snapshots:')
                message_lines.extend('    ' + str(s.relative_to(self.snapshot_dir)) for s in self._updated_snapshots)

            if self._snapshots_to_delete:
                if self._allow_snapshot_deletion:
                    for path in self._snapshots_to_delete:
                        path.unlink()
                    message_lines.append('  Deleted snapshots:')
                else:
                    message_lines.append('  Snapshots that should be deleted: '
                                         '(run pytest with --allow-snapshot-deletion to delete them)')

                message_lines.extend('    ' + str(s.relative_to(self.snapshot_dir)) for s in self._snapshots_to_delete)

            raise AssertionError('\n'.join(message_lines))

    @property
    def snapshot_dir(self):
        return self._snapshot_dir

    @snapshot_dir.setter
    def snapshot_dir(self, value):
        self._snapshot_dir = Path(value).absolute()

    def _snapshot_path(self, snapshot_name: Union[str, Path]) -> Path:
        """
        Returns the absolute path to the given snapshot.
        """
        if isinstance(snapshot_name, Path):
            snapshot_path = snapshot_name.absolute()
        else:
            snapshot_path = self.snapshot_dir.joinpath(snapshot_name)

        if self.snapshot_dir not in snapshot_path.parents:
            raise AssertionError('Snapshot path {} is not in {}'.format(
                shorten_path(snapshot_path), shorten_path(self.snapshot_dir)))

        return snapshot_path

    def assert_match(self, value: str, snapshot_name: Union[str, Path]):
        """
        Asserts that ``value`` equals the current value of the snapshot with the given ``snapshot_name``.

        If pytest was run with the --snapshot-update flag, the snapshot will instead be updated to ``value``.
        The test will fail if the value changed.
        """
        if not isinstance(value, str):
            raise TypeError('value must be str')

        snapshot_path = self._snapshot_path(snapshot_name)

        if snapshot_path.is_file():
            expected_value = snapshot_path.read_text('utf-8')
        elif snapshot_path.exists():
            raise AssertionError('snapshot exists but is not a file: {}'.format(shorten_path(snapshot_path)))
        else:
            expected_value = None

        if self._snapshot_update:
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            if expected_value is not None:
                if expected_value != value:
                    snapshot_path.write_text(value, 'utf-8')
                    self._updated_snapshots.append(snapshot_path)
            else:
                snapshot_path.write_text(value, 'utf-8')
                self._created_snapshots.append(snapshot_path)
        else:
            if expected_value is not None:
                # pytest diffs before version 5.4.0 required expected to be on the left hand side.
                expected_on_right = version.parse(pytest.__version__) >= version.parse("5.4.0")
                try:
                    if expected_on_right:
                        assert value == expected_value
                    else:
                        assert expected_value == value
                except AssertionError as e:
                    snapshot_diff_msg = str(e)
                else:
                    snapshot_diff_msg = None

                if snapshot_diff_msg:
                    snapshot_diff_msg = 'value does not match the expected value in snapshot {}\n{}'.format(
                        shorten_path(snapshot_path), snapshot_diff_msg)
                    raise AssertionError(snapshot_diff_msg)
            else:
                raise AssertionError(
                    "snapshot {} doesn't exist. (run pytest with --snapshot-update to create it)".format(
                        shorten_path(snapshot_path)))

    def assert_match_dir(self, values_by_filename: Dict[str, str], snapshot_dir_name: Union[str, Path]):
        """
        Asserts that the values in values_by_filename equal the current values in the given snapshot directory.

        If pytest was run with the --snapshot-update flag, the snapshots will instead be updated.
        The test will fail there were any changes to the snapshots.
        """
        snapshot_dir_path = self._snapshot_path(snapshot_dir_name)

        if snapshot_dir_path.is_dir():
            existing_names = {p.name for p in snapshot_dir_path.iterdir()}
        elif snapshot_dir_path.exists():
            raise AssertionError('snapshot exists but is not a directory: {}'.format(shorten_path(snapshot_dir_path)))
        else:
            existing_names = set()

        names = set(values_by_filename)
        added_names = names - existing_names
        removed_names = existing_names - names
        if self._snapshot_update:
            self._snapshots_to_delete.extend(snapshot_dir_path.joinpath(name) for name in sorted(removed_names))
        else:
            if added_names or removed_names:
                message_lines = ['Values do not match snapshots in {}'.format(shorten_path(snapshot_dir_path))]
                if added_names:
                    message_lines.append("  Values without snapshots:")
                    message_lines.extend('    ' + s for s in added_names)
                if removed_names:
                    message_lines.append("  Snapshots without values:")
                    message_lines.extend('    ' + s for s in removed_names)
                message_lines.append('  Run pytest with --snapshot-update to update the snapshot directory.')
                raise AssertionError('\n'.join(message_lines))

        # Call assert_match to add, update, or assert equality for all snapshot files in the directory.
        for name, value in values_by_filename.items():
            self.assert_match(value, snapshot_dir_path.joinpath(name))


def shorten_path(path: Path) -> Path:
    """
    Returns the path relative to the current working directory is possible. Otherwise return the path unchanged.
    """
    try:
        return path.relative_to(os.getcwd())
    except ValueError:
        return path


def get_default_snapshot_dir(node: _pytest.python.Function) -> Path:
    """
    Returns the default snapshot directory for the pytest test.
    """
    test_module_dir = node.fspath.dirpath()
    test_module = node.fspath.purebasename
    if '[' not in node.name:
        test_name = node.name
        parametrize_name = None
    else:
        test_name = node.originalname
        parametrize_match = PARAMETRIZED_TEST_REGEX.match(node.name)
        assert parametrize_match is not None, 'Expected request.node.name to be of format TEST_FUNCTION[PARAMS]'
        parametrize_name = PARAMETRIZED_TEST_REGEX.match(node.name).group(1)
        parametrize_name = get_valid_filename(parametrize_name)
    default_snapshot_dir = test_module_dir.join('snapshots', test_module, test_name)
    if parametrize_name:
        default_snapshot_dir = default_snapshot_dir.join(parametrize_name)
    return Path(str(default_snapshot_dir))


def get_valid_filename(s: str) -> str:
    """
    Return the given string converted to a string that can be used for a clean filename.
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
