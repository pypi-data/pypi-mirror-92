import random
from collections import Counter, defaultdict
from typing import List


def analyze_length_count(length_count: dict):
    sorted_count = sorted(length_count.items(), key=lambda kv: kv[0])
    print("Analyze length count:")
    print("\tTotal Count:", *sorted_count)
    pivots = [0.8, 0.9, 0.95, 0.97, 0.98, 0.99, 1.01]
    agg_num = []
    tmp_num = 0
    for k, v in sorted_count:
        tmp_num += v
        agg_num.append(tmp_num)
    print("\tTotal num: ", tmp_num)
    agg_ratio = list(map(lambda x: x / tmp_num, agg_num))
    print("\tRatio: ")
    for pivot in pivots:
        idx = sum(list(map(lambda x: x < pivot, agg_ratio))) - 1
        print("\t\t{} : {}".format(pivot,
                                   "-" if idx == -1 else sorted_count[idx][0]))


def analyze_vocab_count(vocab_count: dict):
    pivots = [0, 1, 2, 3, 4, 5, 10, 20, 30]
    vocab_size = []
    count = []
    for pivot in pivots:
        tmp = list(filter(lambda pair: pair[1] > pivot, vocab_count.items()))
        vocab_size.append(len(tmp))
        count.append(sum(map(lambda pair: pair[1], tmp)))
    print("Analyze vocab count:")
    print("\tTotal vocab size {}, count: {}".format(vocab_size[0], count[0]))
    print("\tRatio: ")
    for cid in range(len(pivots)):
        print("\t\t> {}: vocab size {}/{:.3f}, count {}/{:.3f}".format(
            pivots[cid], vocab_size[cid], vocab_size[cid] / vocab_size[0],
            count[cid], count[cid] / count[0]))


def dump_count(dct: dict, file_path, value_decreasing=True):
    assert not isinstance(dct, Vocab)
    file = open(file_path, "w", encoding="utf8")
    for ele in sorted(dct.items(),
                      key=lambda x: x[1],
                      reverse=value_decreasing):
        print("{} {}".format(ele[0], ele[1]), file=file)
    file.close()


def count_token(lines: List[str]) -> Counter:
    _count = defaultdict(lambda: 0)
    for line in lines:
        arr = line.strip().split()
        for ele in arr:
            _count[ele] += 1
    ret = Counter(dict(_count))
    return ret


class Vocab:
    pad_token, pad_index = "<pad>", 0
    unk_token, unk_index = "<unk>", 1
    bos_token, bos_index = "<bos>", 2
    eos_token, eos_index = "<eos>", 3

    def __init__(self, t2i_dct):
        self.__t2i_dct = t2i_dct
        self.__i2t_dct = {item[1]: item[0] for item in t2i_dct.items()}

    @staticmethod
    def from_count(count, topk=None):
        _t2i_dct = {
            Vocab.bos_token: Vocab.bos_index,
            Vocab.pad_token: Vocab.pad_index,
            Vocab.eos_token: Vocab.eos_index,
            Vocab.unk_token: Vocab.unk_index
        }
        for ele in sorted(count.items(), key=lambda x: x[1], reverse=True):
            _t2i_dct[ele[0]] = len(_t2i_dct)
            if topk is not None and len(_t2i_dct) > topk:
                break
        return Vocab(_t2i_dct)

    def seq2idx(self, seq) -> list:
        return list(
            map(
                lambda x: self.__t2i_dct[x]
                if x in self.__t2i_dct else self.unk_index, seq))

    def idx2seq(self, idx: list, bpe=None):
        if self.pad_index in idx:
            idx = idx[:idx.index(self.pad_index)]
        if self.eos_index in idx:
            idx = idx[:idx.index(self.eos_index)]
        ret = " ".join(list(map(lambda x: self.__i2t_dct[x], idx)))
        if bpe:
            return ret.replace("{} ".format(bpe), "")
        else:
            return ret

    def __getitem__(self, word):
        if word in self.__t2i_dct:
            return self.__t2i_dct[word]
        else:
            return self.unk_index

    def idx2word(self, idx):
        return self.__i2t_dct[idx]

    def __len__(self):
        return len(self.__t2i_dct)

    @property
    def t2i_dct(self):
        return self.__t2i_dct

    @property
    def i2t_dct(self):
        return self.__i2t_dct

    def pad(self):
        return self.pad_index

    def bos(self):
        return self.bos_index

    def eos(self):
        return self.eos_index

    def unk(self):
        return self.unk_index

    def add_token(self, token):
        idx = len(self.__t2i_dct)
        self.__t2i_dct[token] = idx
        self.__i2t_dct[idx] = token


def random_drop(idx: List, drop_rate) -> List:
    assert 0.0 < drop_rate < 0.5
    ret = list(
        filter(lambda x: x is not None,
               map(lambda x: None if random.random() < drop_rate else x, idx)))
    if len(ret) == 0:
        return ret
    return ret


def batch_drop(idx: List[List], drop_rate) -> List[List]:
    return list(map(lambda x: random_drop(x, drop_rate), idx))


def batch_pad(idx: List[List], pad_ele=0, pad_len=None) -> List[List]:
    if pad_len is None:
        pad_len = max(map(len, idx))
    return list(map(lambda x: x + [pad_ele] * (pad_len - len(x)), idx))


def batch_mask(idx: List[List], mask_zero=True) -> List[List]:
    if mask_zero:
        good_ele, mask_ele = 1, 0
    else:
        good_ele, mask_ele = 0, 1
    max_len = max(map(len, idx))
    return list(
        map(lambda x: [good_ele] * len(x) + [mask_ele] * (max_len - len(x)),
            idx))


def batch_mask_by_len(lens: List[int], mask_zero=True) -> List[List]:
    if mask_zero:
        good_ele, mask_ele = 1, 0
    else:
        good_ele, mask_ele = 0, 1
    max_len = max(lens)
    return list(
        map(lambda x: [good_ele] * x + [mask_ele] * (max_len - x), lens))


def batch_append(idx: List[List], append_ele, before=False) -> List[List]:
    if not before:
        return list(map(lambda x: x + [append_ele], idx))
    else:
        return list(map(lambda x: [append_ele] + x, idx))


def batch_lens(idx: List[List]) -> List:
    return list(map(len, idx))


def as_batch(idx: List) -> List[List]:
    return [idx]


def flatten_lst(lst: List[List]) -> List:
    return [i for sub_lst in lst for i in sub_lst]
