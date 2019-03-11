
# ******************************
# @Time    : 3/8/17 3:05 PM
# @Author  : Maggie Fang
# @Software: PyCharm
# @Version : Python3 
# ******************************
import sys
import random
import math
import collections
import csv

random.seed(0)

def load_data():
    bids = collections.defaultdict(dict)
    budgets = {}

    with open('bidder_dataset.csv', 'rt', encoding="utf8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            advertiser = int(row[0])
            query = row[1]
            bid = float(row[2])
            if row[3]:
                budgets[advertiser] = float(row[3])
            bids[query][advertiser] = bid

    queries = []
    with open("queries.txt") as f:
        for line in f:
            queries.append(line.strip())

    return bids, budgets, queries

def getALG(bids, budgets, queries,func):
    revenues = []
    for i in  range(100):
        random.shuffle(queries)
        r = func(bids,budgets,queries)
        revenues.append(r)
    return  float(sum(revenues)/len(revenues))

def greedy(bids, budgets, queries):
    r = 0.0
    tmp = budgets.copy()
    for q in queries:
        candidate = []
        for a in bids[q].keys():
            if tmp[a] >= bids[q][a]:
                candidate.append(a)

        if len(candidate) == 0:
            continue
        candidate.sort()
        choice = max(candidate, key=bids[q].get)

        r += bids[q][choice]
        tmp[choice] -= bids[q][choice]
    return r

def balance(bids, budgets, queries):
    r = 0.0
    tmp = budgets.copy()
    for q in queries:
        candidate = []
        for a in bids[q].keys():
            if tmp[a] >= bids[q][a]:
                candidate.append(a)
        if len(candidate) == 0:
            continue
        candidate.sort()
        choice = max(candidate, key=tmp.get)

        r += bids[q][choice]
        tmp[choice] -= bids[q][choice]
    return r

def mssv(bids, budgets, queries):
    r = 0.0
    tmp = budgets.copy()
    for q in queries:
        candidate = []
        for a in bids[q].keys():
            if tmp[a] >= bids[q][a]:
                candidate.append(a)
        if len(candidate) == 0:
            continue
        candidate.sort()
        fracs = {a: bids[q][a] * (1 - math.exp(-1 * tmp[a] / budgets[a])) for a in candidate}
        choice = max(candidate, key=fracs.get)

        r += bids[q][choice]
        tmp[choice] -= bids[q][choice]
    return r

def main():
    if len(sys.argv) != 2:
        print("usage: python adwords.py <greedy|msvv|balance>")
        exit(1)

    bids, budgets, queries = load_data()
    OPT = sum(budgets.values())
    if sys.argv[1] == "greedy":
        revenue = greedy(bids, budgets, queries)
        ALG = getALG(bids,budgets,queries,greedy)
    elif sys.argv[1] == "mssv":
        revenue= mssv(bids, budgets, queries)
        ALG = getALG(bids, budgets, queries, mssv)
    elif sys.argv[1] == "balance":
        revenue= balance(bids, budgets, queries)
        ALG = getALG(bids, budgets, queries, balance)
    else:
        print("usage: python adwords.py <greedy|msvv|balance>")
        exit(1)

    print("revenue: ", format(revenue, ".2f"))
    print("competitive ratio: ", round(ALG / OPT, 2))

if __name__ == "__main__":
    main()