import re
import get_winamax_data

def get_match_id(urls):
    if isinstance(urls, list):
        urls = " ".join(urls)
    pattern = r'https://www\.winamax\.fr/paris-sportifs/match/(\d+)'
    ids = re.findall(pattern, urls)
    return ids

def get_bet_id(urls, match_ids):
    bet_ids = []
    for url, match_id in zip(urls, match_ids):
        data = get_winamax_data.WinaData(url)
        bet_ids.append(data['matches'][f"{match_id}"]["mainBetId"])
    return bet_ids


