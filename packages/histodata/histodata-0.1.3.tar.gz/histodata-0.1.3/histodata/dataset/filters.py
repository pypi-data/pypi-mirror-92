import random


class DataFrameFilter:
    def __init__(self, mode):
        self.mode = mode

    def __call__(self, df, indices):
        if self.mode == 0:
            return df.iloc[indices]
        elif self.mode == 1:
            return df.loc[~df.index.isin(indices)]
        else:
            return df.iloc[indices], df.loc[~df.index.isin(indices)]


class RandomFilter(DataFrameFilter):
    def __init__(self, percentage_to_filter, mode=0, seed=None):
        super().__init__(mode)
        self.percentage_to_filter = percentage_to_filter
        self.seed = seed

    def __call__(self, df):
        r = random.Random(self.seed)
        indices = r.sample(list(df.index), int(len(df) * self.percentage_to_filter))
        return super().__call__(df, indices)


class LambdaFilter(DataFrameFilter):
    def __init__(self, lambda_function, mode=0):
        super().__init__(mode)
        self.lambda_function = lambda_function

    def __call__(self, df):
        return super().__call__(df, df[df.apply(self.lambda_function, 1)].index)


class ColumnFilter(DataFrameFilter):
    def __init__(self, name_of_column, allowed_values, mode=0):
        super().__init__(mode)
        self.name_of_column = name_of_column
        self.allowed_values = allowed_values

    def __call__(self, df):
        if isinstance(self.allowed_values, list):
            return super().__call__(df, df[df[self.name_of_column].isin(self.allowed_values)].index)
        else:
            return super().__call__(df, df[df[self.name_of_column] == self.allowed_values].index)
