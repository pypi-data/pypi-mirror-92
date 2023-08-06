import pytest

from tests.utils import assert_pytest_passes


@pytest.fixture
def basic_case_dir(testdir):
    case_dir = testdir.mkdir('case_dir')
    dict_snapshot1 = case_dir.mkdir('dict_snapshot1')
    dict_snapshot1.join('obj1.txt').write_text('the value of obj1.txt', 'ascii')
    dict_snapshot1.join('obj2.txt').write_text('the value of obj2.txt', 'ascii')
    return case_dir


def test_assert_match_dir_success(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
                'obj2.txt': 'the value of obj2.txt',
            }, 'dict_snapshot1')
    """)
    assert_pytest_passes(testdir)


def test_assert_match_dir_failure(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
                'obj2.txt': 'the INCORRECT value of obj2.txt',
            }, 'dict_snapshot1')
    """)
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::test_sth FAILED*',
        ">* raise AssertionError(snapshot_diff_msg)",
        'E* AssertionError: value does not match the expected value in snapshot case_dir?dict_snapshot1?obj2.txt',
        "E* assert * == *",
        "E* - the value of obj2.txt",
        "E* + the INCORRECT value of obj2.txt",
        "E* ?    ++++++++++",
    ])
    assert result.ret == 1


def test_assert_match_dir_missing_snapshot(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
                'obj2.txt': 'the value of obj2.txt',
                'new_obj.txt': 'the value of new_obj.txt',
            }, 'dict_snapshot1')
    """)
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::test_sth FAILED*',
        "E* AssertionError: Values do not match snapshots in case_dir?dict_snapshot1",
        'E*   Values without snapshots:',
        'E*     new_obj.txt',
        'E*   Run pytest with --snapshot-update to update the snapshot directory.',
    ])
    assert result.ret == 1


def test_assert_match_dir_missing_value(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
            }, 'dict_snapshot1')
    """)
    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::test_sth FAILED*',
        "E* AssertionError: Values do not match snapshots in case_dir?dict_snapshot1",
        'E*   Snapshots without values:',
        'E*     obj2.txt',
        'E*   Run pytest with --snapshot-update to update the snapshot directory.',
    ])
    assert result.ret == 1


def test_assert_match_dir_update_existing_snapshot_no_change(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
                'obj2.txt': 'the value of obj2.txt',
            }, 'dict_snapshot1')
    """)
    result = testdir.runpytest('-v', '--snapshot-update')
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
    ])
    assert result.ret == 0


@pytest.mark.parametrize('case_dir_repr',
                         ["'case_dir'",
                          "str(Path('case_dir').absolute())",
                          "Path('case_dir')",
                          "Path('case_dir').absolute()"],
                         ids=['relative_string_case_dir',
                              'abs_string_case_dir',
                              'relative_path_case_dir',
                              'abs_path_case_dir'])
@pytest.mark.parametrize('snapshot_name_repr',
                         ["'dict_snapshot1'",
                          "str(Path('case_dir/dict_snapshot1').absolute())",
                          "Path('case_dir/dict_snapshot1')",  # TODO: support this or "Path('dict_snapshot1')"?
                          "Path('case_dir/dict_snapshot1').absolute()"],
                         ids=['relative_string_snapshot_name',
                              'abs_string_snapshot_name',
                              'relative_path_snapshot_name',
                              'abs_path_snapshot_name'])
def test_assert_match_dir_update_existing_snapshot(testdir, basic_case_dir, case_dir_repr, snapshot_name_repr):
    """
    Tests that `Snapshot.assert_match_dir` works when updating an existing snapshot.

    Also tests that `Snapshot` supports absolute/relative str/Path snapshot directories and snapshot paths.
    """
    testdir.makepyfile("""
        from pathlib import Path

        def test_sth(snapshot):
            snapshot.snapshot_dir = {case_dir_repr}
            snapshot.assert_match_dir({{
                'obj1.txt': 'the value of obj1.txt',
                'obj2.txt': 'the NEW value of obj2.txt',
            }}, {snapshot_name_repr})
    """.format(case_dir_repr=case_dir_repr, snapshot_name_repr=snapshot_name_repr))
    result = testdir.runpytest('-v', '--snapshot-update')
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
        '*::test_sth ERROR*',
        "E* AssertionError: Snapshot directory was modified: case_dir",
        'E*   Updated snapshots:',
        'E*     dict_snapshot1?obj2.txt',
    ])
    assert result.ret == 1

    assert_pytest_passes(testdir)  # assert that snapshot update worked


def test_assert_match_dir_create_new_snapshot_file(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
                'obj2.txt': 'the value of obj2.txt',
                'new_obj.txt': 'the value of new_obj.txt',
            }, 'dict_snapshot1')
    """)
    result = testdir.runpytest('-v', '--snapshot-update')
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
        '*::test_sth ERROR*',
        "E* AssertionError: Snapshot directory was modified: case_dir",
        'E*   Created snapshots:',
        'E*     dict_snapshot1?new_obj.txt',
    ])
    assert result.ret == 1

    assert_pytest_passes(testdir)  # assert that snapshot update worked


def test_assert_match_dir_delete_snapshot_file(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
            }, 'dict_snapshot1')
    """)
    result = testdir.runpytest('-v', '--snapshot-update')
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
        '*::test_sth ERROR*',
        "E* AssertionError: Snapshot directory was modified: case_dir",
        'E*   Snapshots that should be deleted: (run pytest with --allow-snapshot-deletion to delete them)',
        'E*     dict_snapshot1?obj2.txt',
    ])
    assert result.ret == 1

    result = testdir.runpytest('-v', '--snapshot-update', '--allow-snapshot-deletion')
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
        '*::test_sth ERROR*',
        'E* AssertionError: Snapshot directory was modified: case_dir',
        'E*   Deleted snapshots:',
        'E*     dict_snapshot1?obj2.txt',
    ])
    assert result.ret == 1

    assert_pytest_passes(testdir)  # assert that snapshot update worked


def test_assert_match_dir_create_new_snapshot_dir(testdir, basic_case_dir):
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({
                'obj1.txt': 'the value of obj1.txt',
            }, 'new_dict_snapshot')
    """)
    result = testdir.runpytest('-v', '--snapshot-update')
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
        '*::test_sth ERROR*',
        'E* AssertionError: Snapshot directory was modified: case_dir',
        'E*   Created snapshots:',
        'E*     new_dict_snapshot?obj1.txt',
    ])
    assert result.ret == 1

    assert_pytest_passes(testdir)  # assert that snapshot update worked


def test_assert_match_dir_existing_snapshot_is_not_dir(testdir, basic_case_dir):
    basic_case_dir.join('file1').write_text('', 'ascii')
    testdir.makepyfile("""
        def test_sth(snapshot):
            snapshot.snapshot_dir = 'case_dir'
            snapshot.assert_match_dir({}, 'file1')
    """)
    result = testdir.runpytest('-v', '--snapshot-update')
    result.stdout.fnmatch_lines([
        '*::test_sth FAILED*',
        "E* AssertionError: snapshot exists but is not a directory: case_dir?file1",
    ])
    assert result.ret == 1
