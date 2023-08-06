from ..helper import helper
from . import transformer_adapter


class Adapter:
    def __init__(self, transfs=None, access_orders=None, is_callable_with_batches=None, seed=None):
        # convert or create list of pre_transformation_adapters
        self.transfs = helper.create_list_from_variable(transfs)

        # create a new access_orders list
        if access_orders is not None:
            if len(self.transfs) != len(access_orders):
                assert AssertionError(
                    "The list of transformers and the list of access_order must be have "
                    + "the same length."
                )
            self.access_orders = access_orders
            for idx, v in enumerate(self.access_orders):
                self.access_orders[idx] = helper.create_list_from_variable(v)
        else:
            self.access_orders = [[] for _ in self.transfs]

        # create a new is_callable_with_batches list
        if is_callable_with_batches is not None:
            if len(self.transfs) != len(is_callable_with_batches):
                assert AssertionError(
                    "The list of transformers and the list of is_callable_with_batches "
                    + "must be have the same length."
                )
            self.is_callable_with_batches = is_callable_with_batches
        else:
            self.is_callable_with_batches = [True for _ in self.transfs]

        self.is_splitters = []

        self.seed = seed

    def append(self, trans, access_order=None, is_callable_with_batches=False, is_splitter=False):
        # TODO, need to check the values
        self.transfs.append(trans)
        self.access_orders.append(access_order)
        if issubclass(type(trans), transformer_adapter.TransformerAdapter):
            self.is_callable_with_batches.append(trans.is_callable_with_batches)
            self.is_splitters.append(trans.is_splitter)
        else:
            self.is_callable_with_batches.append(is_callable_with_batches)
            self.is_splitters.append(is_splitter)

    def __set_values_to_input_dictionary__(self, dictionary, values):
        input_dic = {}
        for k in dictionary:
            input_dic[k] = values[dictionary[k]]
        return input_dic

    def __update_output_dictionary_to_values__(self, dictionary, values, output_values):
        for k_result, k_dictionary in zip(output_values, dictionary):
            values[dictionary[k_dictionary]] = output_values[k_result]
        return values

    def __call_single_transform_with_dict__(
        self, item_or_batch, hashes, transf, dictionary, batch_callable, is_splitter
    ):
        is_batch = isinstance(hashes, list)

        if is_batch is False:
            if self.seed is not None:
                helper.set_random_seed_with_int(int(self.seed + hashes))
            input_dic = self.__set_values_to_input_dictionary__(dictionary, item_or_batch)
            result = transf(**input_dic)
            return self.__update_output_dictionary_to_values__(dictionary, item_or_batch, result)
        elif batch_callable and self.seed is None:
            input_dic = self.__set_values_to_input_dictionary__(dictionary, item_or_batch)
            result = transf(**input_dic)
            item_or_batch.update(result)
            return item_or_batch
        else:
            """
            result = {}
            for i in range(len(item_or_batch[list(item_or_batch)[0]])):
                if self.seed is not None:
                    helper.set_random_seed_with_int(int(self.seed + hashes[j]))
                element
                input_dic = self.__set_values_to_input_dictionary__(dictionary, item_or_batch)
                result = transf(**input_dic)
                item_or_batch.update(result)
            """
            raise NotImplementedError()

    def __call_single_transform_with_callable__(
        self, item_or_batch, hashes, transf, order, batch_callable, is_splitter
    ):
        is_batch = isinstance(hashes, list)

        if order is None or order == [] or order[0] is None or order[0] == "":
            order = list(item_or_batch)

        tmp_saved_seed_state = helper.get_random_seed()

        for i, name in enumerate(order):

            element = item_or_batch.pop(name)

            if is_batch is False:
                if self.seed is not None:
                    helper.set_random_seed_with_int(int(self.seed + hashes))
                result = transf(element)
            elif batch_callable and self.seed is None:
                result = transf(element)
            else:
                result = {}
                for j, item in enumerate(element):
                    if self.seed is not None:
                        helper.set_random_seed_with_int(int(self.seed + hashes[j]))

                    result_item = transf(item)

                    if isinstance(result_item, dict):
                        if j == 0:
                            for k in result_item:
                                result[name + "_" + k] = [result_item[k]]
                        else:
                            for k in result_item:
                                result[name + "_" + k].append(result_item[k])
                    else:
                        if j == 0:
                            result[name] = [result_item]
                        else:
                            result[name].append(result_item)

            if isinstance(result, dict):
                for k in result:
                    if k.startswith(name):
                        item_or_batch[k] = result[k]
                    else:
                        item_or_batch[name + "_" + k] = result[k]
            else:
                item_or_batch[name] = result

            # use the same seed for each data that contains to the same image.
            if i < len(order) - 1:
                helper.set_random_seed(*tmp_saved_seed_state)

        return item_or_batch

    def __call__(self, item_or_batch, hashes):

        if self.seed is not None:
            saved_seed_state = helper.get_random_seed()

        for (transf, order, batch_callable, is_splitter) in zip(
            self.transfs,
            self.access_orders,
            self.is_callable_with_batches,
            self.is_splitters,
        ):
            if isinstance(order, dict):
                item_or_batch = self.__call_single_transform_with_dict__(
                    item_or_batch, hashes, transf, order, batch_callable, is_splitter
                )
            else:
                item_or_batch = self.__call_single_transform_with_callable__(
                    item_or_batch, hashes, transf, order, batch_callable, is_splitter
                )

        if self.seed is not None:
            helper.set_random_seed(*saved_seed_state)

        return item_or_batch
