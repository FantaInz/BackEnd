
from app.models.player import Player
from app.models.squad import Squad
from decimal import Decimal
from tests.fixtures import create_and_delete_database
from app.services.algorithm.utils import create_players_dataframe,encode_squad
from app.services.algorithm.solver import Solver
def dummy_data_init():
    players = []
    player = Player(id=1, name="sth", position=1, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=1, availability=1)
    players.append(player)
    player = Player(id=2, name="sth", position=1, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=1, availability=1)
    players.append(player)
    player = Player(id=3, name="sth", position=2, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=1, availability=1)
    players.append(player)
    player = Player(id=4, name="sth", position=2, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=2, availability=1)
    players.append(player)
    player = Player(id=5, name="sth", position=2, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=2, availability=1)
    players.append(player)
    player = Player(id=6, name="sth", position=2, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=2, availability=1)
    players.append(player)
    player = Player(id=7, name="sth", position=2, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=3, availability=1)
    players.append(player)
    player = Player(id=8, name="sth", position=3, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=3, availability=1)
    players.append(player)
    player = Player(id=9, name="sth", position=3, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=3, availability=1)
    players.append(player)
    player = Player(id=10, name="sth", position=3, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=4, availability=1)
    players.append(player)
    player = Player(id=11, name="sth", position=3, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=4, availability=1)
    players.append(player)
    player = Player(id=12, name="sth", position=3, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=4, availability=1)
    players.append(player)
    player = Player(id=13, name="sth", position=4, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=5, availability=1)
    players.append(player)
    player = Player(id=14, name="sth", position=4, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=5, availability=1)
    players.append(player)
    player = Player(id=15, name="sth", position=4, price=5, points=[1, 2, 3, 4, 5],
                    expectedPoints=[Decimal(1), Decimal(1)],team_id=5, availability=1)
    players.append(player)
    return players


def test_alg_increase_points():
    squad=Squad()
    squad.players=dummy_data_init()
    players=dummy_data_init()
    strong_player=Player(id=16, name="strong", position=1, price=5, points=[1, 2, 3, 4, 5],
                         expectedPoints=[Decimal(2), Decimal(2)],team_id=6, availability=1)
    players.append(strong_player)
    df=create_players_dataframe(players,squad)
    current_squad=encode_squad(16,squad)

    solver=Solver(df,current_squad,16,100,1,1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free= solver.solve()

    assert status==1
    assert transfer_in[0][15].value()==1
    assert squad[0][15].value()==1

def test_alg_decrease_points():
    squad=Squad()
    squad.players=dummy_data_init()
    players=dummy_data_init()
    weak_player=Player(id=16, name="weak", position=1, price=5, points=[1, 2, 3, 4, 5],
                         expectedPoints=[Decimal(0), Decimal(0)],team_id=6, availability=1)
    players.append(weak_player)
    df=create_players_dataframe(players,squad)
    current_squad=encode_squad(16,squad)

    solver=Solver(df,current_squad,16,100,1,1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free= solver.solve()

    assert status==1
    assert transfer_in[0][15].value()==0
    assert squad[0][15].value()==0


def test_alg_keep_pentalty():
    squad=Squad()
    squad.players=dummy_data_init()
    players=dummy_data_init()
    player1=Player(id=16, name="pl1", position=1, price=5, points=[1, 2, 3, 4, 5],
                         expectedPoints=[Decimal(3), Decimal(0)],team_id=6, availability=1)

    player2=Player(id=17, name="pl2", position=2, price=5, points=[1, 2, 3, 4, 5],
                         expectedPoints=[Decimal(3), Decimal(0)],team_id=7, availability=1)
    players.append(player1)
    players.append(player2)
    df=create_players_dataframe(players,squad)
    current_squad=encode_squad(17,squad)

    solver=Solver(df,current_squad,17,100,1,1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free= solver.solve()

    assert status==1
    assert transfer_in[0][15].value()+transfer_in[0][16].value()==1
    assert squad[0][15].value()+squad[0][16].value()==1


def test_alg_wont_go_over_budget():
    squad = Squad()
    squad.players = dummy_data_init()
    players = dummy_data_init()
    expensive = Player(id=16, name="expensive", position=1, price=12, points=[1, 2, 3, 4, 5],
                     expectedPoints=[Decimal(3), Decimal(0)],team_id=6, availability=1)
    players.append(expensive)
    df = create_players_dataframe(players, squad)
    current_squad = encode_squad(16, squad)

    solver = Solver(df, current_squad, 16, 5, 1, 1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = solver.solve()

    for i,el in enumerate(transfer_out[0]):
        if el.value()!=0:
            print(i,el.value())

    assert status == 1
    assert transfer_in[0][15].value() == 0
    assert squad[0][15].value() == 0

def test_alg_max_over_many_weeks():
    squad = Squad()
    squad.players = dummy_data_init()
    players = dummy_data_init()
    early_best = Player(id=16, name="early_best", position=1, price=5, points=[1, 2, 3, 4, 5],
                       expectedPoints=[Decimal(2), Decimal(1)],team_id=6, availability=1)
    overall_best1=Player(id=17, name="early_best", position=2, price=5, points=[1, 2, 3, 4, 5],
                       expectedPoints=[Decimal(1.5), Decimal(3)],team_id=7, availability=1)
    overall_best2=Player(id=18, name="early_best", position=3, price=5, points=[1, 2, 3, 4, 5],
           expectedPoints=[Decimal(1.5), Decimal(3)],team_id=8, availability=1)
    players.append(early_best)
    players.append(overall_best1)
    players.append(overall_best2)
    df = create_players_dataframe(players, squad)
    current_squad = encode_squad(18, squad)

    solver = Solver(df, current_squad, 18, 10, 1, 2,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = solver.solve()

    assert status == 1
    assert transfer_in[0][15].value()+transfer_in[1][15].value() == 0
    assert transfer_in[0][17].value()+transfer_in[1][17].value() >= 1
    assert transfer_in[0][16].value() + transfer_in[1][16].value() >= 1
    assert squad[0][15].value() + squad[1][15].value() == 0
    assert squad[0][17].value()+squad[1][17].value() >= 1
    assert squad[0][16].value() + squad[1][16].value() >= 1


def test_alg_keeps_team_constrain():
    squadD = Squad()
    squadD.players = dummy_data_init()
    players = dummy_data_init()
    tm1 = Player(id=16, name="early_best", position=1, price=5, points=[1, 2, 3, 4, 5],
                       expectedPoints=[Decimal(2), Decimal(2)],team_id=6, availability=1)
    tm2=Player(id=17, name="early_best", position=2, price=5, points=[1, 2, 3, 4, 5],
                       expectedPoints=[Decimal(2), Decimal(2)],team_id=6, availability=1)
    tm3=Player(id=18, name="early_best", position=3, price=5, points=[1, 2, 3, 4, 5],
           expectedPoints=[Decimal(2), Decimal(2)],team_id=6, availability=1)
    tm4 = Player(id=19, name="early_best", position=4, price=5, points=[1, 2, 3, 4, 5],
                  expectedPoints=[Decimal(2), Decimal(2)], team_id=6, availability=1)
    players.append(tm1)
    players.append(tm2)
    players.append(tm3)
    players.append(tm4)
    df = create_players_dataframe(players, squadD)

    current_squad = encode_squad(19, squadD)

    solver = Solver(df, current_squad, 19, 10, 4, 1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = solver.solve()
    teams_ids=df.team_id.tolist()
    positions=df.position.tolist()
    for row in squad:
        res=sum(teammate.value() for teammate, position in zip(row, positions) if position == 4)
        print("RESULT")
        print(res)
    assert status == 1
    assert (transfer_in[0][15].value()+transfer_in[0][16].value()+transfer_in[0][17].value()
            +transfer_in[0][18].value()<= 3)
    assert (squad[0][15].value()+squad[0][16].value()+squad[0][17].value()
            +squad[0][18].value()<= 3)


def test_alg_keeps_position_constrain():
    squadD = Squad()
    squadD.players = dummy_data_init()
    players = dummy_data_init()
    tm1 = Player(id=16, name="early_best", position=1, price=5, points=[1, 2, 3, 4, 5],
                       expectedPoints=[Decimal(2), Decimal(2)],team_id=6, availability=1)
    tm2=Player(id=17, name="early_best", position=1, price=5, points=[1, 2, 3, 4, 5],
                       expectedPoints=[Decimal(2), Decimal(2)],team_id=6, availability=1)
    tm3=Player(id=18, name="early_best", position=1, price=5, points=[1, 2, 3, 4, 5],
           expectedPoints=[Decimal(2), Decimal(2)],team_id=6, availability=1)
    players.append(tm1)
    players.append(tm2)
    players.append(tm3)
    df = create_players_dataframe(players, squadD)
    current_squad = encode_squad(18, squadD)

    solver = Solver(df, current_squad, 18, 10, 3, 1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = solver.solve()

    assert status == 1
    assert (transfer_in[0][15].value()+transfer_in[0][16].value()+transfer_in[0][17].value()<= 2)
    assert (squad[0][15].value()+squad[0][16].value()+squad[0][17].value()<= 2)

def test_alg_must_have_will_join():
    squadD = Squad()
    squadD.players = dummy_data_init()
    players = dummy_data_init()
    tm1 = Player(id=16, name="must", position=1, price=5, points=[1, 2, 3, 4, 5],
                 expectedPoints=[Decimal(0.5), Decimal(0.5)], team_id=6, availability=1)
    players.append(tm1)
    df = create_players_dataframe(players, squadD)
    current_squad = encode_squad(16, squadD)

    solver = Solver(df, current_squad, 16, 10, 1, 1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = solver.solve([15],)

    assert status == 1
    assert transfer_in[0][15].value() ==1
    assert squad[0][15].value() ==1

def test_alg_cat_have_wont_join():
    squadD = Squad()
    squadD.players = dummy_data_init()
    players = dummy_data_init()
    tm1 = Player(id=16, name="must", position=1, price=5, points=[1, 2, 3, 4, 5],
                 expectedPoints=[Decimal(5), Decimal(5)], team_id=6, availability=1)
    players.append(tm1)
    df = create_players_dataframe(players, squadD)
    current_squad = encode_squad(16, squadD)

    solver = Solver(df, current_squad, 16, 10, 1, 1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = solver.solve([],[15])

    assert status == 1
    assert transfer_in[0][15].value() == 0
    assert squad[0][15].value() == 0

def test_alg_unobtainable_constrain_will_break_solution():
    squadD = Squad()
    squadD.players = dummy_data_init()
    players = dummy_data_init()
    tm1 = Player(id=16, name="must", position=1, price=20, points=[1, 2, 3, 4, 5],
                 expectedPoints=[Decimal(5), Decimal(5)], team_id=6, availability=1)
    players.append(tm1)
    df = create_players_dataframe(players, squadD)
    current_squad = encode_squad(16, squadD)

    solver = Solver(df, current_squad, 16, 10, 1, 1,0)
    status, transfer_in, transfer_out, captain, subs, team, squad, free = solver.solve([15],[])

    assert status == -1


