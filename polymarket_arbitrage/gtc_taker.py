import math
import threading
import time
from datetime import datetime

import get_match_data
import get_odd
import get_ev
import send_discord
import order_polymarket
import bet_data_base
from requests_cache import CachedSession

# Contains all the dates of upcoming matches
dates_ref = [
    datetime(2025, 1, 1, 0, 0),
]
# Contains all the Winamax URLs for the matches
winamax_urls = [
    "https://www.winamax.fr/paris-sportifs/match/MATCH_ID",
]
# Contains all the Polymarket URLs for the matches
polymarket_urls = [
    "https://gamma-api.polymarket.com/events/slug/SLUG",
]

def buy_thread(token, mise_best, match_id, type_game, p_best, w_best, size_best, EV_best):
    # Place the bet at a probability 8% lower to account for the approximation of implicit probabilities
    mini_poly = math.floor(w_best - 8)

    # Add 600 shares if the amount of the first order in the order book is less than the optimal bet amount
    if abs(mise_best - size_best) < 1:
        mise_best += math.ceil(600 * round(p_best / 100, 3))

    # Generate the order on Polymarket
    success, errorMsg = order_polymarket.PlaceOrder(token, round(mini_poly / 100, 3), round(mise_best / (p_best / 100), 0))

    # Inform the user about a potential bet on Polymarket
    send_discord.PotentialBuyEmbed(type_game, list(polymarket_data[polymarket_game].keys())[i1], list(polymarket_data[polymarket_game].keys())[i3], p_best, round(w_best, 2), mise_best, size_best, EV_best)
    if success and errorMsg == '':
        if order_polymarket.GetTradesLoop(market_id) == True:
            bet_data_base.AddBet(match_id, token_type, round(1 / (p_best / 100), 2), round(w_best, 2), mise_best)
            send_discord.AcceptBuyEmbed(type_game, list(polymarket_data[polymarket_game].keys())[i1], list(polymarket_data[polymarket_game].keys())[i3], p_best, round(w_best, 2), mise_best, size_best, EV_best)
        else:
            send_discord.DeniedBuyEmbed(type_game, list(polymarket_data[polymarket_game].keys())[i1], list(polymarket_data[polymarket_game].keys())[i3], p_best, round(w_best, 2), mise_best, size_best, "ERROR")
    else:
        send_discord.DeniedBuyEmbed(type_game, list(polymarket_data[polymarket_game].keys())[i1], list(polymarket_data[polymarket_game].keys())[i3], p_best, round(w_best, 2), mise_best, size_best, errorMsg)

is_first = True
while True:
    if is_first:
        is_first = False

        # Retrieve all IDs from the Winamax URLs
        winamax_matchs_id = get_match_data.GetMatchIds(winamax_urls)
        winamax_bets_id = get_match_data.GetBetIds(winamax_urls, winamax_matchs_id)

        # Create request sessions for each Polymarket URL with caching to optimize execution time
        sessions = []
        for polymarket_url in polymarket_urls:
            text = polymarket_url.rsplit("/", 1)[-1]
            session = CachedSession(f"cache/{text}", expire_after = 3600)
            sessions.append(session)

    actual_len = -1
    for winamax_url, polymarket_url in zip(winamax_urls, polymarket_urls):
        start_time = time.time()
        actual_len += 1

        # Check if the match date has started but the match is not finished (approximately 2 hours and 40 minutes)
        actual_date = datetime.now()
        if actual_date < dates_ref[actual_len] or actual_date.timestamp() >= dates_ref[actual_len].timestamp() + 9800:
            continue
        
        # Retrieve the explicit odds for the match
        winamax_data = get_odd.WinamaxData(winamax_url, winamax_matchs_id[actual_len], winamax_bets_id[actual_len])

        # Calculate the implicit probabilities for the matches (approximately)
        if winamax_data != 0:
            for game in winamax_data:
                total = 0
                for player in winamax_data[game]:
                    if winamax_data[game][player]:
                        winamax_data[game][player] = 1 / (winamax_data[game][player])
                    else:
                        winamax_data[game][player] = 0
                    total += winamax_data[game][player]
                for player in winamax_data[game]:
                    if winamax_data[game][player] != 0:
                        winamax_data[game][player] = ((winamax_data[game][player]) / total) * 100
        # Check if we are not in a tense situation where probabilities can change at any moment
        else:
            date_now = datetime.now()
            print(f"X | {date_now}")
            time.sleep(0.4)
            continue

        # Retrieve the odds offered by Polymarket users
        polymarket_data = get_odd.PolymarketData(polymarket_url, sessions[actual_len])
        for winamax_game, polymarket_game in zip(winamax_data.keys(), polymarket_data.keys()):

            # This part is used in case of a mismatch between participants (desynchronization between Winamax and Polymarket)
            if list(polymarket_data[polymarket_game].keys())[0] == "" or list(polymarket_data[polymarket_game].keys())[0] == "":
                i1 = 0
                i2 = 2
                i3 = 1
            elif list(polymarket_data[polymarket_game].keys())[0] == "" or list(polymarket_data[polymarket_game].keys())[0] =="":
                i1 = 1
                i2 = 0
                i3 = 2
            elif list(polymarket_data[polymarket_game].keys())[0] == "" or list(polymarket_data[polymarket_game].keys())[0] == "":
                i1 = 1
                i2 = 2
                i3 = 0
            elif list(polymarket_data[polymarket_game].keys())[0] == "" or list(polymarket_data[polymarket_game].keys())[0] == "":
                i1 = 2
                i2 = 0
                i3 = 1
            elif list(polymarket_data[polymarket_game].keys())[0] == "" or list(polymarket_data[polymarket_game].keys())[0] == "":
                i1 = 2
                i2 = 1
                i3 = 0
            else:
                i1 = 0
                i2 = 1
                i3 = 2
            
            # Simplify the code by creating variables for each value
            w_dom = winamax_data[winamax_game][list(winamax_data[winamax_game].keys())[0]]
            w_draw = winamax_data[winamax_game][list(winamax_data[winamax_game].keys())[1]]
            w_ext = winamax_data[winamax_game][list(winamax_data[winamax_game].keys())[2]]
            p_dom = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['oui'][0]
            p_draw = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['oui'][0]
            p_ext = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['oui'][0]
            p_no_dom = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['non'][0]
            p_no_draw = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['non'][0]
            p_no_ext = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['non'][0]
            dom_size = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['oui'][1]
            draw_size = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['oui'][1]
            ext_size = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['oui'][1]
            no_dom_size = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['non'][1]
            no_draw_size = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['non'][1]
            no_ext_size = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['non'][1]

            # Call the function to retrieve possible opportunities for buying (expected value)
            data = get_ev.getGTCEV(
                w_dom,
                w_draw,
                w_ext,
                p_dom,
                p_draw,
                p_ext,
                p_no_dom,
                p_no_draw,
                p_no_ext,
                list(polymarket_data[polymarket_game].keys())[i1],
                list(polymarket_data[polymarket_game].keys())[i3],
                dom_size,
                draw_size,
                ext_size,
                no_dom_size,
                no_draw_size,
                no_ext_size,
            )
            

            if data != []:
                is_tent = False

                # Retrieve the historical bets for the current match
                match_id = bet_data_base.GenerateMatchId(list(polymarket_data[polymarket_game].keys())[i1], list(polymarket_data[polymarket_game].keys())[i3], dates_ref[actual_len])
                old_data = bet_data_base.GetHistoricalBets(match_id)

                for info in data:
                    name = info[0]
                    wina = info[1]
                    poly = info[2]
                    ev = info[3]
                    mise = info[4]
                    size = info[5]
                    token_type = info[6]
                    mini_poly = math.ceil(wina - 8)

                    # Check if the bet is sufficiently profitable
                    if ev / mise <= 0.1 or abs(wina - poly) < 8:
                        continue

                    # Assign the correct token based on the outcome of the bet
                    if token_type == "yes_dom":
                        token = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['oui'][2]
                        market_id = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['market_id']
                    elif token_type == "yes_draw":
                        token = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['oui'][2]
                        market_id = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['market_id']
                    elif token_type == "yes_ext":
                        token = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['oui'][2]
                        market_id = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['market_id']
                    elif token_type == "no_dom":
                        token = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['non'][2]
                        market_id = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i1]]['market_id']
                    elif token_type == "no_draw":
                        token = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['non'][2]
                        market_id = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i2]]['market_id']
                    elif token_type == "no_ext":
                        token = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['non'][2]
                        market_id = polymarket_data[polymarket_game][list(polymarket_data[polymarket_game].keys())[i3]]['market_id']

                    # Check if the bet is interesting enough to be placed (used only if a bet is already ongoing on the match)
                    if ev / mise >= 1 and old_data != []:
                        for match in old_data:
                            if match['team'] == token_type and match['odd'] == round( 1 / (poly / 100), 2):
                                ev = 0
                    
                    if old_data == [] or (ev/mise >= 1):
                        is_tent = True

                        # Start a new thread to handle the bet placement
                        thread = threading.Thread(target=buy_thread, args=(token, mise, match_id, token_type, poly, wina, size, ev))
                        thread.start()

                # Close the order in case of non-purchase, with error protection
                if is_tent:
                    time.sleep(10)
                    try:
                        order_polymarket.CancelAllOrders()
                    except:
                        print("R1")
                        time.sleep(3)
                        try:
                            order_polymarket.CancelAllOrders()
                        except:
                            print("R2")
                            time.sleep(3)
                            order_polymarket.CancelAllOrders()
                        
        # Limit execution time to avoid overloading the APIs
        temp = time.time()
        if temp - start_time < 0.46:
            sec = 0.46 - float(temp - start_time)
            time.sleep(sec)
