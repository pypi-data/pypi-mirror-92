import ray
import modin
import modin.pandas as pd
import warnings

class HappyPandas:
    """
     Happy Pandas
    """
    def __init__(
        self,
        showAll: bool=False
    ):
        if not ray.is_initialized():
            ray.init(address='auto')

        warnings.filterwarnings('ignore')

        if showAll:
            pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

        self.showAll = showAll
        self.pd = pd

    def get_pd(self):
        return self.pd
