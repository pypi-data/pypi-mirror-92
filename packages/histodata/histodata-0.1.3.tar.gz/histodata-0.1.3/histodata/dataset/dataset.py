import random

import numpy as np
import pandas as pd
import torch
import torch.utils

from ..helper import helper
from . import adapter
from . import data_frame as df_creator
from . import reader


class HistoDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        data_frame_creator: str,
        path_to_dataset: str,
        data_frame_editor=None,
        data_frame_filters=None,
        data_readers: str = None,
        feature_readers: str = None,
        pre_transfs=None,
        da_transfs=None,
        seed: int = None,
        return_data_rows: bool = False,
    ):
        super().__init__()

        # save variables
        self.path_to_dataset = path_to_dataset
        self.return_data_rows = return_data_rows
        self.seed = seed
        self.seed_increment = 0

        # create a DataFrameCreator if str was given
        if isinstance(data_frame_creator, str):
            data_frame_creator = df_creator.CreateDFFromCSV(data_frame_creator)

        # convert or create list of data_readers
        self.data_readers = helper.create_dict_from_variable(data_readers, "data")
        for name in self.data_readers:
            if isinstance(self.data_readers[name], str):
                self.data_readers[name] = reader.ReadFromImageFile(self.data_readers[name])

        # convert or create list of feature_readers
        self.feature_readers = helper.create_dict_from_variable(feature_readers, "feature")
        for name in self.feature_readers:
            if isinstance(self.feature_readers[name], str):
                self.feature_readers[name] = reader.ReadValueFromCSV(self.feature_readers[name])

        # convert or create list of pre_transformation_adapters
        if pre_transfs is None:
            if self.seed is None:
                self.pre_transfs = adapter.Adapter(seed=random.randint(0, 99999999999))
            else:
                self.pre_transfs = adapter.Adapter(seed=self.seed * int(1e3))
        else:
            self.pre_transfs = pre_transfs

        # convert or create list of pre_transformation_adapters
        if da_transfs is None:
            self.da_transfs = adapter.Adapter()
        else:
            self.da_transfs = da_transfs

        # read csv file
        self.df = data_frame_creator(self.path_to_dataset)

        if data_frame_editor is not None:
            self.df = data_frame_editor(
                self.df, self.path_to_dataset, self.data_readers[list(self.data_readers)[0]]
            )

        # filter the df
        if data_frame_filters is not None:
            if isinstance(data_frame_filters, list):
                for df_filter in data_frame_filters:
                    self.df = df_filter(self.df)
            else:
                self.df = data_frame_filters(self.df)

        # make sure that the indizes starts by 0
        self.df.reset_index(inplace=True, drop=True)

        # create hash for each row
        self.df["__hash_of_row__"] = self.df.apply(lambda row: int(hash(str(row.values)) % 1e17), 1)

        # for preloading the images / labels
        self.preloaded_images = None
        self.preloaded_features = None

    def get_feature_for_all_rows(self, feature_pos=None):
        if self.preloaded_images is not None:
            if feature_pos is None:
                return self.preloaded_features
            else:
                return [row[feature_pos] for row in self.preloaded_features]
        else:
            if feature_pos is None:
                return [
                    feature_loader(self.df, self.path_to_dataset)
                    for feature_loader in self.feature_readers
                ]
            else:
                return self.feature_readers[feature_pos](self.df, self.path_to_dataset)

    def preload(self, batch_size=128):
        self.preloaded_images = {}
        self.preloaded_features = {}
        for i in range(0, len(self.df), batch_size):
            img, feat = self.__load__(self.df.iloc[i : i + batch_size].index)
            for k in img:
                if isinstance(img[k], list):
                    img[k] = np.array(img[k])
                if k in self.preloaded_images:
                    if isinstance(img[k], np.ndarray):
                        self.preloaded_images[k] = np.concatenate(
                            [self.preloaded_images[k], img[k]]
                        )
                    else:
                        self.preloaded_images[k] = torch.cat([self.preloaded_images[k], img[k]], 0)
                else:
                    self.preloaded_images[k] = img[k]

            for k in feat:
                if isinstance(feat[k], list):
                    feat[k] = np.array(feat[k])
                if k in self.preloaded_features:
                    if isinstance(feat[k], np.ndarray):
                        self.preloaded_features[k] = np.concatenate(
                            [self.preloaded_features[k], feat[k]]
                        )
                    else:
                        self.preloaded_features[k] = torch.cat(
                            [self.preloaded_features[k], feat[k]], 0
                        )
                else:
                    self.preloaded_features[k] = feat[k]

    def __load__(self, idx):
        # get asked row
        row = self.df.iloc[idx]

        # load data
        images = {}
        for key, img_loader in self.data_readers.items():
            loaded = img_loader(row, self.path_to_dataset)
            if isinstance(loaded, dict):
                for k in loaded:
                    images[key + "_" + k] = loaded[k]
            else:
                images[key] = loaded
        features = {
            key: feature_loader(row, self.path_to_dataset)
            for key, feature_loader in self.feature_readers.items()
        }

        # pre transform
        images = self.pre_transfs(images, self.__get_hash__(idx))

        return images, features

    def __len__(self):
        return len(self.df)

    def __get_hash__(self, idx):
        # get hashes
        row = self.df.iloc[idx]
        hashes = row["__hash_of_row__"]
        if isinstance(hashes, pd.Series):
            hashes = hashes.values.tolist()
        return hashes

    def __getitem__(self, idx):

        # get asked row
        row = self.df.iloc[idx]

        if self.seed is not None:
            # save random state to reactivate this state after the call
            saved_seed_state = helper.get_random_seed()
            # set seets
            helper.set_random_seed_with_int((1 + self.seed_increment) * int(1e9) + self.seed)
            # increase seed increment to use a new random seed at next call
            self.seed_increment += 1

        if self.preloaded_images is None:
            images, features = self.__load__(idx)
        else:
            images = {}
            for k in self.preloaded_images:
                images[k] = self.preloaded_images[k][idx]
            features = {}
            for k in self.preloaded_features:
                features[k] = self.preloaded_features[k][idx]

        # da transforms
        images = self.da_transfs(images, self.__get_hash__(idx))

        if self.seed is not None:
            # reactivate random state
            helper.set_random_seed(*saved_seed_state)

        dic = {}
        dic.update(images)
        dic.update(features)
        if self.return_data_rows:
            dic["raw"] = row
        return dic
