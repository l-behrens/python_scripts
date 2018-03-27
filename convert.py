#!/usr/bin/python
import xlrd
import os
import threading
import asyncio
import itertools
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor

'''
Convert UK Amazon inventory-template spreadsheets to valid flat file
'''

'''maps ctype code to type'''
#types = {1: 'text', 2: 'number', 3: 'date', 4: 'boolean', 5: 'error code', 6:'empty'}


def init(sh):
    '''lookup the Column number of grouping qualifiers'''

    global COLOR
    global SIZE
    global MODEL

    for i1, rx in enumerate(range(sh.nrows)):
        for i2, cx in enumerate(sh.row(rx)):
            if i1 <= 2 and 'model_name' == str(cx.value):
                MODEL = i2
            elif i1 <= 2 and 'color_name' == str(cx.value):
                COLOR = i2
            elif i1 <= 2 and 'size_name' == str(cx.value):
                SIZE = i2

    return (MODEL, COLOR, SIZE)


def make_rules(sh, *args):
    ''' make set of all grouping rules '''
    s = set()
    for i in args:
        t = list(args)
        t.remove(i)
        if len(t) > 1:
            s = s.union(make_rules(sh, *t))
    return set(itertools.permutations(args)).union(s)


def product_matrix(sh):
    ''' converts excel sheet into product matrix '''
    products = []
    for i1, rx in enumerate(range(3, sh.nrows)):
        tmp = []
        for i2, cx in enumerate(sh.row(rx)):

            '''keyword field must be smaller than 250 Bytes'''
            if i1 > 2 and i2 == 44:  # col 44 contains generic_keywords
                buf = cx.value.split(' ')
                while len(' '.join(buf)) > 100:
                    buf.pop()
                tmp.append(' '.join(buf))
                continue

            if cx.ctype == 2:
                tmp.append(str(int(cx.value)))
            elif cx.ctype == 3:
                tmp.append(str(float(cx.value)))
            elif cx.ctype == 4:
                tmp.append(str(bool(cx.value)))
            else:
                tmp2 = str(cx.value).replace('\n', '')
                tmp.append(tmp2)
        products.append(tmp)
    return products


def make_partitions_iterative(rule, prods):
    ''' generate domain dictionary for all permutations of categories
    to the rule'''

    leaves = []
    tree = {}
    for i in range(1, len(rule)+1):
        domains = itertools.product(*[q_sets[r] for r in rule[:i]])

        for d in domains:
            dom = '/'.join(list(d))
            if [l for l in leaves if dom.startswith(l)]:
                continue

            tree[dom] = prods
            for j, d_part in enumerate(d):
                if rule[j] == COLLECTION:
                    tree[dom] = [prod for prod in tree[dom]
                                 if prod[MODEL].startswith(d_part)]
                elif rule[j] == MODEL:
                    tree[dom] = [prod for prod in tree[dom]
                                 if prod[MODEL].endswith(d_part)]
                else:
                    tree[dom] = [prod for prod in tree[dom]
                                 if prod[rule[j]] == d_part]
            if len(tree[dom]) == 0:
                leaves.append(dom)
                tree.pop(dom)
            elif len(tree[dom]) < 15:
                leaves.append(dom)
            else:
                tree.pop(dom)
    return tree


def create_q_sets(qualifiers):
    '''generate category value for all qualifiers '''
    q_sets = {}

    def q_set(qualifier): return set(
        [sh.row(rx)[qualifier].value for rx in range(3, sh.nrows)])

    def c_empty(in_set): return set([value.strip()
                                     for value in in_set if value])

    for qualifier in qualifiers:
        if qualifier == COLLECTION:
            q_sets[qualifier] = set([value.split(' ')[0]
                                     for value in q_set(MODEL)])
        elif qualifier == MODEL:
            q_sets[qualifier] = set([' '.join(value.split(' ')[1:])
                                     for value in q_set(qualifier)])
        else:
            q_sets[qualifier] = q_set(qualifier)

        q_sets[qualifier] = c_empty(q_sets[qualifier])

    return q_sets


def create_group_pages(path, tree):
    pass


if __name__ == "__main__":

    partitions = []
    tree = {}
    prods = []
    qualifiers = []

    global q_sets
    global COLOR
    global SIZE
    global MODEL
    global COLLECTION

    q_sets = {}
    COLOR = 0
    SIZE = 0
    MODEL = 0
    COLLECTION = 'COLLECTION'

    # Input - Output Files
    tdl = 'flat.txt'
    book = xlrd.open_workbook(filename='inventory.xlsx')
    sh = book.sheet_by_name('UK')

    # Qualifier Initialization. Qualifiers are Columns of a Product Matrix. E.g Color
    (MODEL, COLOR, SIZE) = init(sh)
    qualifiers = [MODEL, COLOR, SIZE, COLLECTION]

    # retrieve Categories from Qualifiers. E.g q_sets[Color] = [Red, Silver, Orange,...]
    q_sets = create_q_sets(qualifiers)

    # Matrix representation of all Products in the Excel sheet
    prods = product_matrix(sh)

    # Permutations of all Possible Qualifier selections. (Binomial coeficient of n=len(qualifiers), k=n)
    rules = list(itertools.permutations(qualifiers))

    # apply partition algo to all length(rule) permutations of qualifiers
    with ThreadPoolExecutor(max_workers=8) as e:
        futures = [e.submit(make_partitions_iterative, rule, prods)
                   for rule in rules[:1]]

    # aggregate partitions to one domain tree. Every key will be a parent product page once
    for f in futures:
        r = f.result()
        for res in r:
            if res in tree:
                set(tree[res]).add(set(res.values()))
            else:
                tree[res] = set(res.values())

    print('finished')

    exit(0)

########################################################
#    with open(tdl, 'w') as f:
#        for i1, rx in enumerate(range(sh.nrows)):
#            tmp = []
#            for i2, cx in enumerate(sh.row(rx)):
#
#                '''keyword field must be smaller than 250 Bytes'''
#                if i1 > 2 and i2 == 44: # col 44 contains generic_keywords
#                    buf = cx.value.split(' ')
#                    while len(' '.join(buf)) > 100:
#                        buf.pop()
#                    tmp.append(' '.join(buf))
#                    continue
#
#                if cx.ctype == 2:
#                    tmp.append(str(int(cx.value)))
#                elif cx.ctype == 3:
#                    tmp.append(str(float(cx.value)))
#                elif cx.ctype == 4:
#                    tmp.append(str(bool(cx.value)))
#                else:
#                    tmp2 = []
#                    for p in str(cx.value):
#                        tmp2.append(p.strip())
#                    tmp.append(''.join(tmp2))
#            f.write('\t'.join(tmp))
#            f.write('\n')
