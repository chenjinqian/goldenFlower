#!/usr/bin/env python
# -*- coding: utf-8 -*-


class goldenFlower(object):
    def __init__(self):
        """
        golden flower
        "\u2660" -> "\u2663"
        ♠♡♣♢
        ♠    Spade
        ♡    Heart
        ♣    Club
        ♢    Diamond
        """
        self.d = self.make_d()
        self.card_s = self.make_card()
        self.card_d = self.make_card("d")

    def make_d(self):
        nc_lst = "2,3,4,5,6,7,8,9,10,J,Q,K,A,♢,♣,♡,♠".split(",")
        d = dict([[i, j] for i, j in zip(nc_lst, range(len(nc_lst)))])
        return d

    def make_card(self, how="s"):
        nub_lst = "2,3,4,5,6,7,8,9,10,J,Q,K,A".split(",")
        clo_lst = "♢,♣,♡,♠".split(",")
        card_s =["%s%s"%(i, j) for i in nub_lst for j in clo_lst]
        if how == "s":
            return card_s
        else:
            card_d = dict([[i, ""] for i in card_s])
            return card_d

    def evalue_card(self, card_3):
        """
        ♠♡♣♢
        1 baoZi,         3♠|3♡|3♣
        2 tongHuaShun,   3♢|4♢|5♢
        3 tongHua,       3♢|4♢|6♢
        4 shunZi,        3♢|4♢|5♣
        5 duiZi,         3♢|3♢|5♣
        6 danZhang,      3♢|4♢|6♣
        """
        d = self.d
        cd1, cd2, cd3 = sorted(list(card_3.split("|")), key=lambda x: (d[x[:-1]], d[x[-1]]))
        # maybe like "10♣|3♢|4♢"
        nub_1, clo_1 = cd1[:-1], cd1[-1]
        nub_2, clo_2 = cd2[:-1], cd2[-1]
        nub_3, clo_3 = cd3[:-1], cd3[-1]
        is_baoZi = bool(nub_1 == nub_2 == nub_3)
        is_shunZi = bool(d[nub_2] - d[nub_1] == 1 and d[nub_3] - d[nub_2] == 1)
        is_tongHua = bool(clo_1 == clo_2 and clo_2 == clo_3)
        is_duiZi = bool(nub_1 == nub_2 or nub_2 == nub_3)
        if is_baoZi:
            return [10 - 1, d[nub_1], d[clo_1]]
        if is_tongHua:
            if is_shunZi:
                return [10 - 2, d[nub_3], d[clo_3]]
            else:
                return [10 - 3, d[nub_3], d[nub_2], d[nub_1], d[clo_3]]
        else:
            if is_shunZi:
                return [10 - 4, d[nub_3], d[clo_3]]
            else:
                if is_duiZi:
                    if nub_1 == nub_2:
                        return [10 - 5, d[nub_1], d[nub_3], d[clo_2]]
                    else:
                        return [10 - 5, d[nub_3], d[nub_1], d[clo_3]]
                else:
                    return [10 - 6, d[nub_3], d[nub_2], d[nub_1], d[clo_3]]

    def compare(self, card_a, card_b):
        return card_a > card_b

    def make_card_combine(self):
        # 22100
        card_lst = self.card_s
        rlt = self.combine(card_lst, k=3)
        return rlt

    def combine(self, lst, k=3):
        rlt = []
        lenlst = len(lst)
        if not lenlst:
            return rlt
        flag_lst = [i for i in range(k)]
        pt = 1
        # flag_pointer
        flag_loop = True
        while flag_loop:
            rlt.append([lst[i] for i in flag_lst])
            while flag_lst[- pt] == lenlst - pt:
                pt += 1
                if pt == len(flag_lst) + 1:
                    flag_loop = False
                    break
            if flag_loop:
                # init flag_lst after pt
                pt_init = pt - 1
                flag_lst[- pt] += 1
                while pt_init > 0:
                    flag_lst[- pt_init] = flag_lst[- pt] + pt - pt_init
                    pt_init -= 1
                pt = 1
        rlt_join = ["|".join(i) for i in rlt]
        return rlt_join

    def serve(self):
        pass


def main():
    gf = goldenFlower()
    ccl = gf.make_card_combine()
    ccl_sorted = sorted(ccl, key=lambda x: gf.evalue_card(x))
    assert(len(ccl_sorted) == (52 * 51 * 50 / 6))
    return ccl_sorted


if __name__ == '__main__':
    main()
