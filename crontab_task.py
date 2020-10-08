import json
import time

from app.utils import timeit, get_order_code
from ext_app import db
from manager import app

from app.models import JCRanking, JCTicket, JCRace, Accounts, Races, Orders, PointTrace, League, Team

VOTE_DICT = {
    "1": [
        "1:0",
        "2:0",
        "2:1",
        "3:0",
        "3:1",
        "3:2",
        "4:0",
        "4:1",
        "4:2",
        "5:0",
        "5:1",
        "5:2"
    ],
    "X": [
        "0:0",
        "1:1",
        "2:2",
        "3:3"
    ],
    "2": [
        "0:1",
        "0:2",
        "0:3",
        "0:4",
        "0:5",
        "1:2",
        "1:3",
        "1:4",
        "1:5",
        "2:3",
        "2:4",
        "2:5"
    ]
}


def handle_race(race):
    """
    处理订单详情以及比分
    :param race:
    :return:
    """
    league = League.query.filter(League.league_id == race.league_id).first().en_name
    home = Team.query.filter(Team.team_id == race.home_id).first().en_name
    guest = Team.query.filter(Team.team_id == race.guest_id).first().en_name
    host_score, guest_score = json.loads(race.scores) if race.scores else ("", "")
    scores = ":".join([host_score, guest_score])
    if not host_score and not guest_score:
        scores = ""
    elif int(host_score) > int(guest_score):
        if scores not in VOTE_DICT.get("1"):
            scores = "1 else"
    elif int(host_score) == int(guest_score):
        if scores not in VOTE_DICT.get("X"):
            scores = "X else"
    else:
        if scores not in VOTE_DICT.get("2"):
            scores = "2 else"
    return [league, home, guest], scores


def settle_ticket(race, is_delete=0):
    """
    结算下注以及生成订单以及流水
    :param race:
    :param is_delete:
    :return:
    """
    order_desc, scores = handle_race(race)
    jc_tickets = JCTicket.query.filter(JCTicket.rid == race.race_id, JCTicket.status == 1).all()
    item_list = []
    cat = time.time()
    if is_delete:
        for jc_ticket in jc_tickets:
            order_desc_ = " ".join(order_desc + [jc_ticket.vote])
            jc_ticket.status = 2
            jc_ticket.settle_at = cat
            jc_ticket.settle_number = jc_ticket.number
            jc_ticket.result = "C"
            account = Accounts.query.filter(Accounts.user_id == jc_ticket.uid).first()
            account.available = account.available + jc_ticket.settle_number

            rank = JCRanking.query.filter(JCRanking.user_id == jc_ticket.uid, JCRanking.race_id == race.race_id).first()
            rank.settle_num = jc_ticket.number

            order_num = get_order_code()
            order = Orders(
                user_id=jc_ticket.uid,
                order_num=order_num,
                create_at=cat,
                pay_time=cat,
                number=jc_ticket.settle_number,
                desc=order_desc_,
                source="Pick'em Canceled(score)"
            )
            pt = PointTrace(
                user_id=jc_ticket.uid,
                create_at=cat,
                points=jc_ticket.settle_number,
                desc=order_desc_,
                way="Pick'em Canceled(score)",
                title="Pick'em Canceled(score)",
                order_num=order_num,
                current=account.available,
            )
            item_list.append(pt)
            item_list.append(order)
    else:
        won_ticket = [i for i in jc_tickets if i.vote == scores]
        print(f"won {len((won_ticket))}")
        for won in won_ticket:
            order_desc_ = " ".join(order_desc + [won.vote])
            won.status = 2
            won.settle_at = time.time()
            won.settle_number = int(won.number * won.odds)
            won.result = "W"
            account = Accounts.query.filter(Accounts.user_id == won.uid).first()
            account.available = account.available + won.settle_number

            rank = JCRanking.query.filter(JCRanking.user_id == won.uid, JCRanking.race_id == race.race_id).first()
            rank.settle_num = won.settle_number
            rank.title = f"{order_desc[1]} {scores.split(':')[0]}-{scores.split(':')[1]} {order_desc[2]}"
            order_num = get_order_code()
            order = Orders(
                user_id=won.uid,
                order_num=order_num,
                create_at=cat,
                pay_time=cat,
                number=won.settle_number,
                desc=order_desc_,
                source="Pick'em Return(score)"
            )
            pt = PointTrace(
                user_id=won.uid,
                create_at=cat,
                points=won.settle_number,
                desc=order_desc_,
                way="Pick'em Return(score)",
                title="Pick'em Return(score)",
                order_num=order_num,
                current=account.available,
            )
            item_list.append(pt)
            item_list.append(order)
        lose_ticket = [i for i in jc_tickets if i.vote != scores]
        print(f"lose {len((lose_ticket))}")

        for lose in lose_ticket:
            lose.status = 2
            lose.settle_at = time.time()
            lose.settle_number = 0
            lose.result = "L"
            rank = JCRanking.query.filter(JCRanking.user_id == lose.uid, JCRanking.race_id == race.race_id).first()
            rank.title = f"{order_desc[1]} {scores.split(':')[0]}-{scores.split(':')[-1]} {order_desc[2]}"

    return jc_tickets + item_list


@timeit
def main():
    with app.app_context():
        jc_races = JCRace.query.filter(JCRace.selected == 1, JCRace.settled == 0).all()
        print(jc_races)
        if jc_races:
            for jc_race in jc_races:
                race = Races.query.filter(Races.race_id == jc_race.race_id).first()
                print(race.race_id, race.scores)
                ticket_list = []
                if race.is_delete == 1:
                    # 比赛取消 结算jcticket,更新排行榜,锁定jc_race
                    ticket_list = settle_ticket(race, is_delete=1)
                    jc_race.settled = 1
                elif race.is_started == 2:
                    # 比赛结束 结算jcticket,更新排行榜,锁定jc_race
                    ticket_list = settle_ticket(race)
                    jc_race.settled = 1
                db.session.bulk_save_objects(ticket_list)
                db.session.commit()
                db.session.close()


if __name__ == '__main__':
    main()
