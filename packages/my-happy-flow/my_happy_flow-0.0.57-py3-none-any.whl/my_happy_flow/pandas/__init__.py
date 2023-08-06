from modin.pandas import DataFrame

from my_happy_flow import version

from my_happy_flow.pandas.happy_pandas import HappyPandas

__version__ =  version.get_version()


__all__ = [
    "__version__"
]


def left_align(df: DataFrame):
    """
        left align of the table content
    """
    left_aligned_df = df.style.set_properties(**{'text-align': 'left'})
    left_aligned_df = left_aligned_df.set_table_styles(
        [dict(selector='th', props=[('text-align', 'left')])]
    )
    return left_aligned_df


def count_info(df: DataFrame):
    count_info = "\nrows {rows} x columns {columns}\n".format(
        rows = df.shape[0],
        columns = df.shape[1]
    )
    return count_info
