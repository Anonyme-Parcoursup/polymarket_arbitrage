import get_winamax_data
import requests

def polymarket_data(url, session):
    bd = {}
    response = session.get(url)
    if response.status_code != 200:
        print(f"Erreur: {response.status_code}")
    data = response.json()
    name = data['title']
    bd[name] = {}
    for market in data['markets']:
        market_id = market['conditionId']
        title = market['groupItemTitle']
        tokenIds = eval(market['clobTokenIds'])
        token_yes = tokenIds[0]
        token_no = tokenIds[1]
        token_url = f"https://clob.polymarket.com/book?token_id={token_yes}"
        book_response = requests.get(token_url)
        if book_response.status_code != 200:
            print(f"Erreur: {book_response.status_code}")
            continue
        book_data = book_response.json()
        if book_data['asks']:
            best_yes = round(float(book_data['asks'][-1]['price']) * 100, 1)
            best_yes_size = round(float(book_data['asks'][-1]['size']), 2)
        else:
            best_yes = 100
            best_yes_size = 0
        if book_data['bids']:
            best_no = 100-round(float(book_data['bids'][-1]['price']) * 100, 1)
            best_no_size = round(float(book_data['bids'][-1]['size']), 2)
        else:
            best_no = 100
            best_no_size = 0

        infos_yes = [best_yes, best_yes_size, token_yes]
        infos_no = [best_no, best_no_size, token_no]
        bd[name][title] = {"oui": infos_yes, "non": infos_no, "market_id": market_id}
    return bd
def winamax_data(url, match_id, bet_id):
    bd = {}
    data = get_winamax_data.WinaData(url)
    try:
        if data['matches'][f"{match_id}"]["status"] == "ENDED":
            return 0
    except:
        return 0
    match_name = data['matches'][f"{match_id}"]['title']
    try:
        outcomes = data['bets'][f"{bet_id}"]['outcomes']
        if data['bets'][f"{bet_id}"]['available'] == False:
            return 0
    except:
        return 0
    bd[match_name] = {}
    for outcome in outcomes:
        outcome_name = data['outcomes'][f"{outcome}"]['label']
        outcome_odd = data['odds'][f"{outcome}"]
        bd[match_name][outcome_name] = outcome_odd
    return bd