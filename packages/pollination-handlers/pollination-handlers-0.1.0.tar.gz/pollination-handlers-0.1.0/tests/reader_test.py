from pollination_handlers.outputs.read_file import read_DF_from_path


def test_read_df():
    res = read_DF_from_path('./tests/assets/df_results.res')
    assert res == [25.1, 0, 10, 100]
