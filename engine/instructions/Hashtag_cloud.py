import numpy as np
import pandas as pd


class Hashtag_cloud():
    db = None
    __hashtag_cloud = []
    __link_data = None

    def __init__(self, db):
        self.db = db

    def get_tags(self, link_tags=[], all_tags=[]):
        row = [0] * len(all_tags)
        pos = 0
        for i in all_tags:
            if i in link_tags:
                row[pos] = 1
            pos += 1
        return pd.Series(row, index=all_tags)

    def get_hashtag_with_links(self, data, parameter_confims=[]):
        hashtag_to_ret = {}
        elem_is_add = None
        for i in parameter_confims:
            data = data[data[i] == 1]
        data = data.drop(columns=parameter_confims)
        cur_data = data[data.sum(axis=1) > 0]
        if cur_data.shape[0]:
            data_sum = cur_data.sum()
            keys = data_sum.sort_values(ascending=False)
            for key in keys.index:
                temp_index = pd.Series(data=data[data[key] == 1].index)
                if elem_is_add is None:
                    elem_is_add = pd.Series()
                temp_temp = temp_index[~temp_index.isin(elem_is_add)]
                if temp_temp.shape[0]:
                    hashtag_to_ret.setdefault(key, list(temp_index))
                    data = data.drop(columns=[key])
                    elem_is_add = pd.concat([elem_is_add, temp_temp])
        return hashtag_to_ret

    @property
    def link_data(self):
        if self.__link_data is None:
            all_links = self.db.Instruction.get_all_instruction()
            all_tags_dict = {i.id: [b.tag for b in i.tags] for i in all_links}
            all_tags = np.array(list(all_tags_dict.values()))
            all_tags = np.unique(np.concatenate(all_tags))
            all_tags = pd.Series(all_tags)
            all_links_ids = pd.Series(list(all_tags_dict.keys()))
            all_links_with_hastag = {i: self.get_tags(link_tags=all_tags_dict[i], all_tags=all_tags) for i in all_links_ids}
            big_data = pd.DataFrame.from_dict(all_links_with_hastag, orient="index", columns=all_tags)
            self.__link_data = big_data
            print('Загрузили ссылки из базы')
        return self.__link_data

    def reload_link_data(self):
        self.__link_data = None
        self.link_data
