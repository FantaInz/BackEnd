import numpy as np
import pandas as pd
import pulp
def encode_squad(playersNum,squad):
    arr=np.zeros(playersNum)
    for player in squad.players:
        arr[player.id-1]=1
    return arr

def get_decision_array(name,playersNum,weeks):
    return np.array(
        [
            [
            pulp.LpVariable(f"{name}_{i}_{j}", lowBound=0, upBound=1, cat="Integer")
            for i in range(playersNum)
            ] for j in range(weeks)
        ]
    )

def create_players_dataframe(players,squad):
    df=pd.DataFrame.from_records([d.to_dict() for d in players])
    df['buy_price']=df.price
    df['sell_price']=df.price
    squad.transfers.sort(key=lambda x:x.gameWeek)
    for transfer in squad.transfers:
        id=transfer.inPlayerId-1
        curr_price=df["price"][id]
        buy_price=transfer.inPlayerPrice
        if curr_price<=buy_price:
            new_price=curr_price
        else:
            new_price= (buy_price+curr_price)*5//10
        df.loc[id,"sell_price"]=new_price
    df=df.drop(columns=["price"])
    return df

def decode_decision_array(decision_array,playersNum):
    res=[]
    for i in range(playersNum):
        if decision_array[i].value()!=0:
            res.append(i+1)
    return res
