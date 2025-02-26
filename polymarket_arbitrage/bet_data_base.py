import hashlib
import pandas as pd

def add_bet(match_id, team, odd, proba, amount):
    id = generate_id()
    bet = {
        "id": [id],
        "match_id": [match_id],
        "team": [team],
        "odd": [odd],
        "proba": [proba],
        "amount": [amount],
    }
    new_df = pd.DataFrame(bet)
    df = pd.read_csv("BetDataBase.csv")
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv("bet_data_base.csv", index=False)
    return id

def get_historical_bet(match_id):
    df = pd.read_csv("BetDataBase.csv")
    historical_bets = df[df['match_id'] == match_id]
    bet_list = historical_bets.to_dict(orient='records')
    return bet_list

def generate_id():
    try:
        df = pd.read_csv("BetDataBase.csv")
        if not df.empty:
            last_id = df['id'].max()
            return last_id + 1
        else:
            return 0
    except FileNotFoundError:
        return 0

def generate_match_id(dom, ext, date):
    match_string = f"{dom}-{ext}-{date.isoformat()}"
    match_hash = hashlib.md5(match_string.encode()).hexdigest()
    return match_hash