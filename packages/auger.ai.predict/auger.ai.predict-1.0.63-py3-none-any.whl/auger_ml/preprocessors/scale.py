import operator

from auger_ml.preprocessors.base import BasePreprocessor
import logging

import numpy as np

class ScalePreprocessor(BasePreprocessor):
    def __init__(self, params):
        super(ScalePreprocessor, self).__init__(
            params=params,
            params_keys=[]
        )

    def fit(self, df):
        super(ScalePreprocessor, self).fit(df)

        min_ = df.min()
        max_ = df.max()

        self._min = min_.to_dict()
        self._max = (max_ - min_).to_dict()

        # TODO: handle cases when `_max == 0`

    def transform(self, df):
        super(ScalePreprocessor, self).transform(df)

        df.astype(float, copy=False)

        self.op(df, operator.isub, self._min)
        self.op(df, operator.truediv, self._max)

        #df = df.astype(np.float16, copy=False)

        return df

    @staticmethod
    def op(df, op, values):
        try:
            if op == operator.truediv:
                df /= values
            else:    
                op(df, values)
        except ValueError:
            #assert set(df.columns.values) == set(values.keys())
            for k, v in values.items():
                if op == operator.truediv:
                    df[k] /= v
                else:    
                    op(df[k], v)
