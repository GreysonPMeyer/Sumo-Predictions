import pandas as pd
import numpy as np
import queue

df1 = pd.read_csv('/Users/greysonmeyer/Documents/GitHub/Sumo-Predictions/sumo-wrestling-matches-results-1985-2019/versions/1/1983.csv')

def clean_sumo_data(df, fight_log, rikishi_list, q_dict):
    # Remove duplicate fights
    df = df[~df['rikishi1_rank'].str.endswith('e')]

    # Remove columns that I don't care about
    df = df.drop(['index', 'basho', 'day', 'kimarite', 'rikishi1_id', 'rikishi2_id', 'rikishi2_win'], axis = 1)

    df['prev_history'] = 0
    df['rank_difference'] = 0
    df['upset_comparison'] = 0

    for index, row in df.iterrows():

        # Update fight_log
        i = rikishi_list.index(row['rikishi1_shikona'])
        j = rikishi_list.index(row['rikishi2_shikona'])
        df.loc[index, 'prev_history'] = fight_log[i][j]
        
        if row['rikishi1_win'] == 1:
            fight_log[i][j] += 1
            fight_log[j][i] -= 1
        else:
            fight_log[i][j] -= 1
            fight_log[j][i] += 1        

        # Calculate difference in rank
        if row['rikishi1_rank'][1] == 's':
            rank1 = 0
        elif row['rikishi1_rank'][0] == 'J':
            if row['rikishi1_rank'][-1] == 'D':
                rank1 = 15 - int(row['rikishi1_rank'][1:-3])
            else:
                rank1 = 15 - int(row['rikishi1_rank'][1:-1])
        elif row['rikishi1_rank'][0] == 'M':
            if row['rikishi1_rank'][-1] == 'D':
                rank1 = 32 - int(row['rikishi1_rank'][1:-3])
            else:
                rank1 = 32 - int(row['rikishi1_rank'][1:-1])
        elif row['rikishi1_rank'][0] == 'K':
            rank1 = 35
        elif row['rikishi1_rank'][0] == 'S':
            rank1 = 40
        elif row['rikishi1_rank'][0] == 'O':
            rank1 = 45
        else:
            rank1 = 50

        if row['rikishi2_rank'][1] == 's':
            rank2 = 0
        elif row['rikishi2_rank'][0] == 'J':
            if row['rikishi2_rank'][-1] == 'D':
                rank2 = 15 - int(row['rikishi2_rank'][1:-3])
            else:
                rank2 = 15 - int(row['rikishi2_rank'][1:-1])
        elif row['rikishi2_rank'][0] == 'M':
            if row['rikishi2_rank'][-1] == 'D':
                rank2 = 32 - int(row['rikishi2_rank'][1:-3])
            else:
                rank2 = 32 - int(row['rikishi2_rank'][1:-1])
        elif row['rikishi2_rank'][0] == 'K':
            rank2 = 35
        elif row['rikishi2_rank'][0] == 'S':
            rank2 = 40
        elif row['rikishi2_rank'][0] == 'O':
            rank2 = 45
        else:
            rank2 = 50

        df.loc[index, 'rank_difference'] = rank1 - rank2

        # Calculates upsets
        sum1 = 0
        temp = queue.Queue()

        while not q_dict[row['rikishi1_shikona']].empty():
            item = q_dict[row['rikishi1_shikona']].get()
            sum1 += item
            temp.put(item)

        while not temp.empty():
            q_dict[row['rikishi1_shikona']].put(temp.get())

        sum2 = 0

        while not q_dict[row['rikishi2_shikona']].empty():
            item = q_dict[row['rikishi2_shikona']].get()
            sum2 += item 
            temp.put(item) 

        while not temp.empty():
            q_dict[row['rikishi2_shikona']].put(temp.get())

        df.loc[index, 'upset_comparison'] = sum1 - sum2

        if rank1 > rank2:
            if row['rikishi1_win'] == 0:
                q_dict[row['rikishi1_shikona']].put(-1)
                q_dict[row['rikishi2_shikona']].put(1)
            else:
                q_dict[row['rikishi1_shikona']].put(0)
                q_dict[row['rikishi2_shikona']].put(0)


        if rank1 < rank2:
            if row['rikishi1_win'] == 1:
                q_dict[row['rikishi1_shikona']].put(1)
                q_dict[row['rikishi2_shikona']].put(-1)
            else:
                q_dict[row['rikishi1_shikona']].put(0)
                q_dict[row['rikishi2_shikona']].put(0)
            
        if q_dict[row['rikishi1_shikona']].qsize() > 15:
            q_dict[row['rikishi1_shikona']].get()

        if q_dict[row['rikishi2_shikona']].qsize() > 15:
            q_dict[row['rikishi2_shikona']].get()

    return df, fight_log, q_dict

# Create a matrix to keep track of previous fight history. This should be done after I have merged all of the
# datasets together
rikishi_1 = df1['rikishi1_shikona'].unique()
rikishi1_list = rikishi_1.tolist()
rikishi_2 = df1['rikishi2_shikona'].unique()
rikishi2_list = rikishi_2.tolist()
rikishi_list = rikishi1_list + rikishi2_list
fight_log = np.zeros((len(rikishi_list), len(rikishi_list)))

# Create a queue dictionary to be utilized between datasets
q_dict = dict()
for r in rikishi_list:
    if r not in q_dict.keys():
        q_dict[r] = queue.Queue()

ultimate_df, fight_log, q_dict = clean_sumo_data(df1, fight_log, rikishi_list, q_dict)

for i in range(1984, 2020):
    df = pd.read_csv(f'/Users/greysonmeyer/Documents/GitHub/Sumo-Predictions/sumo-wrestling-matches-results-1985-2019/versions/1/{i}.csv')
    
    for r in df['rikishi1_shikona']:
        if r not in rikishi_list:
            rikishi_list.append(r)
            fight_log = np.column_stack((fight_log, np.zeros(fight_log.shape[0])))
            fight_log = np.vstack((fight_log, np.zeros(fight_log.shape[1])))
            q_dict[r] = queue.Queue()
    for r in df['rikishi2_shikona']:
        if r not in rikishi_list:
            rikishi_list.append(r)
            fight_log = np.column_stack((fight_log, np.zeros(fight_log.shape[0])))
            fight_log = np.vstack((fight_log, np.zeros(fight_log.shape[1])))
            q_dict[r] = queue.Queue()
    
    cleaned_df, fight_log, q_dict = clean_sumo_data(df, fight_log, rikishi_list, q_dict)
    ultimate_df = pd.concat([ultimate_df, cleaned_df], ignore_index=True)
    print(i, ' is complete!')

ultimate_df.to_csv('/Users/greysonmeyer/Downloads/ultimate_sumo_dataset.csv', index=False)