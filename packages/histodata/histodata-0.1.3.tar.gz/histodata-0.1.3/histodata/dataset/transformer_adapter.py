import copy

import numpy as np


class TransformerAdapter:
    def __init__(self):
        self.is_callable_with_batches = False
        self.is_splitter = False

    def __call__(self, img_or_imgs):
        pass


class RandomPrinterAdapter(TransformerAdapter):
    def __init__(self, message="RandomPrinterAdapter:"):
        super().__init__()
        self.message = message
        self.is_callable_with_batches = True
        self.is_splitter = False

    def __call__(self, img_or_imgs):
        print(self.message, np.random.random())
        return img_or_imgs


class CopyAdapter(TransformerAdapter):
    def __init__(self, num_of_copies=2):
        super().__init__()
        self.is_callable_with_batches = True
        self.is_splitter = True
        self.num_of_copies = num_of_copies

    def __call__(self, img_or_imgs):
        result = {}
        for i in range(self.num_of_copies):
            # TODO
            # result.append(img_or_imgs.clone())
            result[str(i)] = copy.copy(img_or_imgs)
        return result
