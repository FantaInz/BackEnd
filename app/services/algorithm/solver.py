import pulp
import numpy as np
import pandas as pd
from app.services.algorithm.utils import get_decision_array
class Solver:
    def __init__(self,df,current_squad,playerNum,budget,freeTransfers,weeks):
        self.df=df
        self.current_squad=current_squad
        self.playerNum=playerNum
        self.budget=budget
        self.freeTransfers=freeTransfers
        self.positions = df.position.tolist()
        self.teams_ids = df.team_id.tolist()
        self.pl_teams = df.team_id.unique()
        self.weeks=weeks

    def create_decision_arrays(self):
        free_in = get_decision_array("free_in", self.playerNum,self.weeks)
        paid_in = get_decision_array("paid_in", self.playerNum,self.weeks)
        transfer_out = get_decision_array("transfer_out", self.playerNum,self.weeks)
        transfer_in = free_in + paid_in
        captain = get_decision_array("captain", self.playerNum,self.weeks)
        subs = get_decision_array("subs", self.playerNum,self.weeks)
        return free_in, paid_in, transfer_out, transfer_in, captain, subs

    def add_transfer_constrains(self,model,free_in, transfer_out, transfer_in, budget_now,week):
        model += sum(free_in) <= self.freeTransfers+week
        in_cost = sum(transfer_in * self.df.price.tolist())
        out_cost = sum(transfer_out * self.df.price.tolist())
        budget_next_week = budget_now + out_cost - in_cost
        model += budget_next_week >= 0
        return budget_next_week

    def add_squad_constrains(self,model,squad,subs,team,captain):
        for i in range(0, self.playerNum):
            model += squad[i] - subs[i] >= 0
            model += team[i] - captain[i] >= 0
            model += team[i] + subs[i] <= 1

        model += sum(squad) == 15
        model += sum(team) == 11
        model += sum(captain) == 1
        model += sum(subs) == 4

        # goalkeeper
        model = + sum(squadmate for squadmate, position in zip(squad, self.positions) if position == 1) == 2
        model += sum(teammate for teammate, position in zip(team, self.positions) if position == 1) == 1
        # defender

        model = + sum(squadmate for squadmate, position in zip(squad, self.positions) if position == 2) == 5
        model += sum(teammate for teammate, position in zip(team, self.positions) if position == 2) >= 3
        model += sum(teammate for teammate, position in zip(team, self.positions) if position == 2) <= 5
        # midfielder

        model = + sum(squadmate for squadmate, position in zip(squad, self.positions) if position == 3) == 5
        model += sum(teammate for teammate, position in zip(team, self.positions) if position == 3) >= 3
        model += sum(teammate for teammate, position in zip(team, self.positions) if position == 3) <= 5
        # forward
        model = + sum(squadmate for squadmate, position in zip(squad, self.positions) if position == 4) == 3
        model += sum(teammate for teammate, position in zip(team, self.positions) if position == 4) >= 1
        model += sum(teammate for teammate, position in zip(team, self.positions) if position == 4) <= 3

        # clubs
        for pl_team in self.pl_teams:
            model += sum(squadmate for squadmate, team_id in zip(squad, self.teams_ids) if team_id == pl_team) <= 3


    def extract_expected_points(self,id):
        return np.array(
            pd.DataFrame(self.df.expectedPoints.values.tolist(), index=self.df.id)
            .apply(pd.to_numeric, downcast="float").iloc[:,
            id].tolist())

    def add_objective(self, captain, team, paid_in, expected_points):
        penalty = sum(paid_in) * 4
        return sum(team * expected_points) + sum(captain * expected_points) - penalty

    def solve(self):
        model=pulp.LpProblem("FPL", pulp.LpMaximize)
        cum_obj=0
        (free_in_all,paid_in_all,transfer_out_all,
         transfer_in_all, captain_all, subs_all)=self.create_decision_arrays()
        current_squad=self.current_squad
        budget=self.budget
        team_all=[]
        squad_all=[]
        for week in range(self.weeks):
            transfer_in =transfer_in_all[week]
            free_in =free_in_all[week]
            transfer_out =transfer_out_all[week]
            paid_in =paid_in_all[week]
            captain =captain_all[week]
            subs=subs_all[week]

            squad=current_squad+transfer_in-transfer_out
            squad_all.append(squad)
            team=squad-subs
            team_all.append(team)
            new_budget=self.add_transfer_constrains(model,free_in,transfer_out,transfer_in,budget,week)
            expected_points = self.extract_expected_points(week)
            self.add_squad_constrains(model,squad,subs,team,captain)
            cum_obj+=self.add_objective(captain, team, paid_in, expected_points)
            current_squad=squad
            budget=new_budget

        model+=(sum(sum(free_in_all)))<=self.freeTransfers+self.weeks-1
        model+=cum_obj,"Objective"
        model.solve()
        return transfer_in_all,transfer_out_all,captain_all,subs_all,team_all,squad_all,free_in_all

