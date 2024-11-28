import pulp
import numpy as np
import pandas as pd
import sys

from app.services.algorithm.utils import get_decision_array

class Solver:
    def __init__(self,df,current_squad,playerNum,budget,freeTransfers,weeks,currentWeek):
        self.df=df
        self.current_squad=current_squad
        self.playerNum=playerNum
        self.budget=budget
        self.freeTransfers=freeTransfers
        self.positions = df.position.tolist()
        self.teams_ids = df.team_id.tolist()
        self.pl_teams = df.team_id.unique()
        self.weeks=weeks
        self.currentWeek=currentWeek

    def create_decision_arrays(self):
        free_in = get_decision_array("free_in", self.playerNum,self.weeks)
        paid_in = get_decision_array("paid_in", self.playerNum,self.weeks)
        transfer_out = get_decision_array("transfer_out", self.playerNum,self.weeks)
        transfer_in = free_in + paid_in
        captain = get_decision_array("captain", self.playerNum,self.weeks)
        subs = get_decision_array("subs", self.playerNum,self.weeks)
        return free_in, paid_in, transfer_out, transfer_in, captain, subs

    def add_transfer_constrains(self,model,free_in, transfer_out, transfer_in, budget_now,week):
        in_cost = sum(transfer_in * self.df.buy_price.tolist())
        out_cost = sum(transfer_out * self.df.sell_price.tolist())
        budget_next_week = budget_now + out_cost - in_cost
        model += budget_next_week >= 0
        return budget_next_week

    def _get_pos_limits(self,pos):
        if pos==1:
            return 1,1,2
        elif pos==2:
            return 3,5,5
        elif pos==3:
            return 3,5,5
        elif pos==4:
            return 1,3,3

    def add_positions_and_pl_teams_constrains(self,model,squad,subs,team,captain,week):
        #POSITIONS
        for pos in range(1, 5):
            low, up, sq = self._get_pos_limits(pos)
            model += (
                    sum(
                        teammate
                        for teammate, position in zip(team, self.positions)
                        if position == pos
                    )
                    >= low
            )
            model += (
                    sum(
                        teammate
                        for teammate, position in zip(team, self.positions)
                        if position == pos
                    )
                    <= up
            )
            model += (
                    sum(
                        squadmate
                        for squadmate, position in zip(squad, self.positions)
                        if position == pos
                    )
                    == sq
            )
        #TEAM
        for pl_team in self.pl_teams:
            model += (sum(selected for selected, team_id in zip(squad, self.teams_ids) if team_id == pl_team) <= 3)

        #SIZE
        model += sum(team) == 11
        model += sum(squad) == 15
        model += sum(captain) == 1

        for i in range(self.playerNum):
            model += (team[i] - captain[i]) >= 0
            model += (team[i] + subs[i]) <= 1


    def extract_expected_points(self,id):
        return np.array(
            pd.DataFrame(self.df.expectedPoints.values.tolist(), index=self.df.id)
            .apply(pd.to_numeric, downcast="float").iloc[:,
            id+self.currentWeek].tolist())

    def add_objective(self, captain, team, paid_in,subs,expected_points):
        penalty = sum(paid_in) * 4
        curr_obj=sum(team * expected_points) + sum(captain * expected_points) - penalty
        return curr_obj

    def add_custom_constrains(self,model,squad,must_have,cant_have):
        for player_id in must_have:
            model+=squad[player_id]==1
        for player_id in cant_have:
            model+=squad[player_id]==0

    def add_free_transfer_constrains(self,model,free,cumFree,week):
        max_free=self.freeTransfers+week
        model+=sum(free)<=5
        model+=sum(free)+cumFree<=max_free
        return cumFree+sum(free)


    def solve(self,must_have=[],cant_have=[]):
        model=pulp.LpProblem("FPL", pulp.LpMaximize)
        cum_obj=0
        (free_in_all,paid_in_all,transfer_out_all,
         transfer_in_all, captain_all, subs_all)=self.create_decision_arrays()
        current_squad=self.current_squad
        budget=self.budget
        team_all=[]
        squad_all=[]
        cumFreeTransfers=0
        for week in range(self.weeks):
            transfer_in =transfer_in_all[week]
            free_in =free_in_all[week]
            transfer_out =transfer_out_all[week]
            paid_in =paid_in_all[week]
            captain =captain_all[week]
            subs=subs_all[week]
            #out only of current squad
            for i in range(self.playerNum):
                model+=current_squad[i]-transfer_out[i]>=0

            squad=current_squad+transfer_in-transfer_out
            squad_all.append(squad)
            team=squad-subs
            team_all.append(team)
            self.add_custom_constrains(model,squad,must_have,cant_have)
            new_budget=self.add_transfer_constrains(model,free_in,transfer_out,transfer_in,budget,week)
            expected_points = self.extract_expected_points(week)
            self.add_positions_and_pl_teams_constrains(model,squad,subs,team,captain,week)
            cumFreeTransfers = self.add_free_transfer_constrains(model, free_in, cumFreeTransfers, week)
            cum_obj+=self.add_objective(captain, team, paid_in,subs,expected_points)

            current_squad=squad
            budget=new_budget

        model+=cum_obj,"Objective"
        status=model.solve(pulp.PULP_CBC_CMD())
        return status,transfer_in_all,transfer_out_all,captain_all,subs_all,team_all,squad_all,free_in_all

