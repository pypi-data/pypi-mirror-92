import pytest
from transparentpath import TransparentPath
from pathlib import Path
import pandas as pd
from tablewriter import TableWriter

df = pd.read_csv(Path("tests") / "data" / "input.csv", index_col=0)


@pytest.mark.parametrize(
    "cls", [Path, TransparentPath, str]
)
def test_tablewriter_from_dataframe(cls):
    table = TableWriter(
        path_output=cls("tests/data/ouput"),
        data=df,
        to_latex_args={"column_format": "lrr"},
        label="tab::example",
        caption="TableWriter example",
        hide_numbering=True,
    )
    table.compile(silenced=False)
    if cls == str:
        cls = Path
    assert cls("tests/data/ouput.tex").is_file()
    assert cls("tests/data/ouput.pdf").is_file()
    cls("tests/data/ouput.pdf").unlink()
    cls("tests/data/ouput.tex").unlink()


@pytest.mark.parametrize(
    "cls", [Path, TransparentPath, str]
)
def test_tablewriter_from_file(cls):
    table = TableWriter(
        path_output=cls("tests/data/ouput_from_file"),
        path_input=cls("tests/data/input.csv"),
        label="tab::example",
        caption="TableWriter example",
        read_from_file_args={"index_col": 0},
        number=3,
    )
    if cls == str:
        cls = Path
    table.compile(silenced=False)
    assert cls("tests/data/ouput_from_file.tex").is_file()
    assert cls("tests/data/ouput_from_file.pdf").is_file()
    cls("tests/data/ouput_from_file.pdf").unlink()
    cls("tests/data/ouput_from_file.tex").unlink()
