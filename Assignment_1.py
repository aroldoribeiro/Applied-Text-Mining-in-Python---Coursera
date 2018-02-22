import pandas as pd
import numpy as np

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
mon_num ={"Jan":1,"Feb":2 , "Mar":3, "Apr":4, "May":5,"Jun":6,"Jul":7,"Aug":8, "Sep":9,"Oct":10,"Nov":11,"Dec":12}


def date_sorter():
    
    df = pd.Series(doc)
    mon_num ={"Jan":1,"Feb":2 , "Mar":3, "Apr":4, "May":5,"Jun":6,"Jul":7,"Aug":8, "Sep":9,"Oct":10,"Nov":11,"Dec":12}


    group1 = df.str.findall(r'([0-9]{1,2})(?:[-/,.]+)([0-9]{1,2})(?:[-/,.]+| )([0-9]{2,4})').str[0]
    group1 = group1.dropna()
    group1 = group1.apply(lambda x: (int(x[1]), int(x[0]), int(x[2])) if int(x[2]) >= 1900 and int(x[2]) <= 2050
                              else (int(x[1]), int(x[0]), int('19'+x[2])))

    group2 = df.str.findall(r'(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec){1}[a-z.,]*)(?:[-/.,]| )([0-9]{1,2})(?:[-/,. ]+)([0-9]{2,4})').str[0]
    group2 = group2.dropna()
    group2 = group2.apply(lambda x: (int(x[1]),mon_num[x[0]],int(x[2])) if int(x[2]) >= 1900 else (int(x[1]),mon_num[x[0]],int('19'+x[2])))

    group3 = df.str.findall(r'([0-9]{1,2})(?:[-/,.]+| |)(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec){1}[a-z.,]*)(?:[-/,.]+| )([0-9]{2,4})').str[0]
    group3 = group3.dropna()
    group3 = group3.apply(lambda x: (int(x[0]),mon_num[x[1]],int(x[2])))

    group4 = df.str.findall(r'(?<![0-9]{2} )(?<![0-9]{1})(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec){1}[a-z.,]*)(?:[-/.,]| )([0-9]{4})').str[0]
    group4 = group4.dropna()
    group4 = group4.apply(lambda x: (1, mon_num[x[0]], int(x[1]))  if int(x[1]) >= 1900 else (1,mon_num[x[0]],int('19'+x[1])))

    group5 = df.str.findall(r'(?<![0-9/])(?<!(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|ber|ust){1} )([0-9]{1,2})(?:[-/,.]| )([0-9]{4})').str[0]
    group5 = group5.dropna()
    group5 = group5.apply(lambda x: (1, int(x[0]), int(x[1])))

    group6 = df.str.findall(r'([0-9]{4})').str[0]
    group6 = group6.dropna()
    group6 = group6.loc[[x for x in list(group6.index) if x not in (list(group1.index) + list(group2.index)
                                                        + list(group3.index)
                                                        + list(group4.index)
                                                        + list(group5.index))]]
    group6 = group6.apply(lambda x: (1, 1, int(x)))

    group_list = [group1, group2, group3, group4, group5, group6]

    dic_groups = {}
    for group in group_list:
        for index in group.index:
            dic_groups[index] = group[index]
    dic_groups

    new_df = pd.DataFrame.from_dict(dic_groups, orient="index").rename(columns={0:"day", 1:"mon", 2:"year"})
    ans = new_df.sort_values(["year", "mon","day"], ascending=True).reset_index()['index']
    return ans
