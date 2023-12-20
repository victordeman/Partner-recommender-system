#Install packages
# pip install numpy
# pip install pandas
# pip install sklearn
# pip install igraph
# pip install networkx
# pip install leidenalg
#pip install mysql
#pip install sqlalchemy

#Import otherfiles from this project
import datainput
from graphPruning2.pruning import unimodal
from graphPruning2.pruning import utils

#Import packages
import networkx as nx
import sklearn
import igraph as ig
import leidenalg as la
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 40)
pd.set_option('display.max_rows', 500)

#Import in-built python modules
import random
import itertools
import warnings
warnings.filterwarnings("ignore")

#Loading raw data and preprocessing

sourcequest = [datainput.commrole_data,datainput.extint_data,datainput.manageppl_data,datainput.optimpessim_data,datainput.successrsk_data,datainput.toughtend_data]

#for Extro or Intro file
str_to_id = {0: {'Alone.': 0, 'As part of a team.': 1, 'No strong preference.': 2},
             1: {'I can take them or leave them.': 0, 'Very little.': 1, 'Very much.': 2},
             2: {'A surprise party with lots of family and friends.': 0, 'Going out for a meal with a few family or friends.': 1, 'I prefer my birthday to be just like any other normal day.': 2},
             3: {'In a group discussion.': 0, 'No strong preference.': 1, 'On a one-to-one basis.': 2},
             4: {'Extremely quickly.': 0, 'Fairly quickly.': 1, 'Not very quickly, as I am able to apply my mind to, and concentrate on, the task in hand.': 2},
             5: {'Maybe not a long conversation but I might exchange a few pleasantries with them.': 0, 'Not really.': 1, 'Yes I would really enjoy having a lengthy conversation with them.': 2},
             6: {'As often as possible.': 0, 'Hardly ever at all, as that is not really my idea of enjoyment.': 1, 'Just occasionally.': 2},
             7: {'It wouldn’t worry me, although I may be a little nervous beforehand.': 0, 'No, as I would be very nervous.': 1, 'Yes, I would relish the prospect.': 2},
             8: {'Fairly easily.': 0, 'Not easily.': 1, 'Very easily.': 2},
             9: {'By letter or email.': 0, 'By telephone.': 1, 'Face to face.': 2},
             10: {'I don’t venture on the dance floor if I can avoid it.': 0, 'I tend to go with the flow and join in more or less at the same time as everyone else.': 1, 'Usually one of the first.': 2},
             11: {'A bit of both, depending on the situation or circumstances.': 0, 'Generally a follower.': 1, 'Generally a leader.': 2},
             12: {'I would accept, and would not expect to have any problem': 0, 'I would probably accept, but say that I might not be able to sell them all.': 1, 'I would probably have to decline, as I would be unlikely to sell them.': 2},
             13: {'Hopefully.': 0, 'I doubt it.': 1, 'Perhaps, in certain ways.': 2}, 14: {'I would not wish to become the next chairperson.': 0, 'I would probably push to become the next chairperson.': 1, 'a)\tI may consider the position of chairperson, but only if approached by one of the other     committee members to stand for election': 2},
             15: {'Frequently.': 0, 'Only when pressed to do so.': 1, 'Whenever I feel it is necessary.': 2},
             16: {'No': 0, 'Perhaps so, occasionally.': 1, 'Yes': 2},
             17: {'Cautious.': 0, 'Popular.': 1, 'Tenacious.': 2},
             18: {'It’s OK.': 0, 'No, I hate small talk and can never think of anything to say.': 1, 'Yes, I am quite comfortable when making small talk.': 2},
             19: {'Face-to-face.': 0, 'No preference.': 1, 'Over the telephone.': 2},
             20: {'Maybe.': 0, 'No.': 1, 'Yes.': 2},
             21: {'Balanced.': 0, 'Effervescent.': 1, 'Shy.': 2},
             22: {'No, in any case I don’t have a party piece that I could perform.': 0, 'Not particularly, but I will join in the fun rather than be seen as a party pooper.': 1, 'Yes.': 2},
             23: {'I would like to think so, but I’m not sure I could pluck up the courage.': 0, 'No way.': 1, 'Yes.': 2},
             24: {'No, I cannot say that I do, as there is always lots to ask people.': 0, 'Not usually.': 1, 'Yes, I do sometimes tend to dry up after a while.': 2}}

class Dataset():
    def __init__(self, sourcequest):
        self.sourcequest = sourcequest

    # Extro or Intro
    def extro_data(self):

        for quest in self.sourcequest[1:2]:

            df = quest.drop(['trial',1], axis=1)

            nan_value = float("NaN")
            df = df.replace("", nan_value)
            df = df.dropna()
            #i->question, c->response value
            for i, c in enumerate(df.columns[1:]):
                #taking the question i and assigning corresponding three options from str_to_id
                question = str_to_id[i]
                #depending on the response c replace it with s from question
                df[c] = [question[s] for s in df[c]]
                # print(col_temp)

            df = df.astype('int64')
            #summing all the rows except first row(student id) for each student response to get their transformed questionnaire score
            df['Extro_Total'] = df.iloc[:, 1:].sum(axis=1)

        extro_df = df[['UserID', 'Extro_Total']]
        return extro_df

    # Optimist or Pessimist
    def optim_data(self):

        for quest in self.sourcequest[3:4]:

            df = quest.drop(['trial',1], axis=1)

            nan_value = float("NaN")
            df = df.replace("", nan_value)
            df = df.dropna()
            df = df.astype('int64')

            df = df.replace([0, 1, 3, 4], [4, 3, 1, 0])

            df['Optimist_Total'] = df.iloc[:, 1:].sum(axis=1)


        optimist_df = df[['UserID', 'Optimist_Total']]
        return optimist_df

    # Communicating and Role
    def comm_data(self):

        for quest in self.sourcequest[0:1]:

            df = quest.drop(['trial',1], axis=1)

            nan_value = float("NaN")
            df.replace("", nan_value, inplace=True)
            df.dropna(inplace=True)
            df = df.astype('int64')

            df = df.replace([0, 1, 3, 4], [4, 3, 1, 0])

            df['Communicating_Total'] = df.iloc[:, 1:].sum(axis=1)


        communicating_df = df[['UserID', 'Communicating_Total']]
        return communicating_df

    # Success and Risk
    def success_data(self):

        for quest in self.sourcequest[4:5]:

            df = quest.drop(['trial',1], axis=1)

            nan_value = float("NaN")
            df.replace("", nan_value, inplace=True)
            df.dropna(inplace=True)
            df = df.astype('int64')

            df = df.replace([0, 1, 3, 4], [4, 3, 1, 0])

            df['Success_Total'] = df.iloc[:, 1:].sum(axis=1)


        success_df = df[['UserID', 'Success_Total']]
        return success_df

    # Tough or Tender
    def tough_data(self):

        for quest in self.sourcequest[5:6]:

            df = quest.drop(['trial',1], axis=1)

            nan_value = float("NaN")
            df.replace("", nan_value, inplace=True)
            df.dropna(inplace=True)
            df = df.astype('int64')

            df['Tough_Total'] = df.iloc[:, 1:].sum(axis=1)

        tough_df = df[['UserID', 'Tough_Total']]
        return tough_df

    # Managing People and Resources
    def managing_data(self):

        for quest in self.sourcequest[2:3]:

            df = quest.drop(['trial',1], axis=1)

            nan_value = float("NaN")
            df = df.replace("", nan_value)
            df = df.dropna()
            df = df.astype('int64')

            df.iloc[:, 1:6] = df.iloc[:, 1:6].replace([0, 1, 3, 4], [4, 3, 1, 0])

            df['Managing_People_Total'] = df.iloc[:, 1:].sum(axis=1)


        managing_df = df[['UserID', 'Managing_People_Total']]
        return managing_df




    def result_dataframe(self):

        result1 = pd.merge(self.extro_data(), self.tough_data(), how="inner", on="UserID")

        column_names = ['UserID', 'Extro_Total', 'Tough_Total']
        result1 = result1.reindex(columns=column_names)

        result2 = pd.merge(result1, self.managing_data(), how="inner", on="UserID")

        result3 = pd.merge(result2, self.optim_data(), how="inner", on="UserID")

        result4 = pd.merge(result3, self.comm_data(), how="inner", on="UserID")

        result5 = pd.merge(result4, self.success_data(), how="inner", on="UserID")

        main_df = result5

        return main_df


# success_df_dataset_final = Dataset(sourcequest).success_data()
# print(success_df_dataset_final)

main_dataset = Dataset(sourcequest)
main_dataset_f = main_dataset.result_dataframe()
#Drop students whose grouping details are missing. Can be skipped if details of students are present
ungrouped = [2135,2157,2158,2173]
main_dataset_f = main_dataset_f[~main_dataset_f.UserID.isin(ungrouped)]
main_dataset_final = main_dataset_f.reset_index(drop=True)
print(main_dataset_final)




