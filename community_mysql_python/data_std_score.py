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
import data_process

#Import packages
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import MinMaxScaler

#Import in-built python modules
import itertools
import warnings
warnings.filterwarnings("ignore")

norm_main_df = data_process.main_dataset_final
class std_score():
    #Apply normalization on survey scores

    def normalization_data(norm_data):

        norm_data[['Extro_Total','Tough_Total',\
        'Managing_People_Total','Optimist_Total','Communicating_Total','Success_Total']]\
        = MinMaxScaler().fit_transform(norm_data[['Extro_Total','Tough_Total',\
        'Managing_People_Total','Optimist_Total','Communicating_Total','Success_Total']])

        return norm_data

    norm_data_final = normalization_data(norm_main_df)

    #Transpose main dataframe before calculating difference
    def transpose_data(transp_data):
        # Transpose main dataframe before calculating difference
        dff = transp_data.set_index('UserID').T
        return dff

    # Calculation of distances(differences) between User scores for all surveys
    # For all combinations, calculate differences in scores
    transpose_data_final = transpose_data(norm_data_final)

    def difference(df):
        comb = list(itertools.combinations(df.columns, 2))

        new_df = pd.DataFrame()

        for a, b in comb:
            new_df[f"{a},{b}"] = abs(1 / (df[a] - df[b]))
            new_df = new_df.replace([np.inf, -np.inf], 50)

            new_df = new_df.astype('int64')
        new_df = new_df.transpose()

        new_df = new_df.reset_index(level=0)
        new_df = new_df.rename(columns={"index": "UserID"}, errors="raise")
        return new_df



    result_df = difference(transpose_data_final)

    # print(result_df)

    result_df[['source', 'target']] = result_df['UserID'].str.split(',', expand=True)
    resultdf_extro = result_df[['source', 'target', 'Extro_Total']]
    resultdf_extro = resultdf_extro.rename(columns={'Extro_Total': 'weight'})
    resultdf_optim = result_df[['source', 'target', 'Optimist_Total']]
    resultdf_optim = resultdf_optim.rename(columns={'Optimist_Total': 'weight'})
    resultdf_tough = result_df[['source', 'target', 'Tough_Total']]
    resultdf_tough = resultdf_tough.rename(columns={'Tough_Total': 'weight'})
    resultdf_manage = result_df[['source', 'target', 'Managing_People_Total']]
    resultdf_manage = resultdf_manage.rename(columns={'Managing_People_Total': 'weight'})
    resultdf_comm = result_df[['source', 'target', 'Communicating_Total']]
    resultdf_comm = resultdf_comm.rename(columns={'Communicating_Total': 'weight'})
    resultdf_success = result_df[['source', 'target', 'Success_Total']]
    resultdf_success = resultdf_success.rename(columns={'Success_Total': 'weight'})

    result_df1 = result_df.drop(['UserID'], axis=1)

    #print(result_df)



diff_data_final = std_score.result_df1

#print(diff_data_final)
