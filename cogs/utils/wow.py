import requests

region_info = {
    "US": {"api_url": "https://us.api.battle.net/",
           "locales": ["en_US", "es_MX", "pt_BR"]},
    "EU": {"api_url": "https://eu.api.battle.net/",
           "locales": ["en_GB", "es_ES", "fr_FR", "ru_RU", "de_DE", "pt_PT", "it_IT"]},
    "KR": {"api_url": "https://kr.api.battle.net/",
           "locales": ["ko_KR"]},
    "TW": {"api_url": "https://tw.api.battle.net/",
           "locales": ["zh_TW"]},
    "CN": {"api_url": "https://api.battlenet.com.cn/",
           "locales": ["zh_CN"]},
    "SEA": {"api_url": "https://sea.api.battle.net/",
            "locales": ["en_US"]},
}

# 0 = api_url (from above)
# 1 = realm
# 2 = character name
# 3 = locale
# 4 = api key
request_pattern = "{0}/wow/character/{1}/{2}?locale={3}&apikey={4}"


def get_realm_slug(realm):
    return realm.lower().replace(' ', '-').replace("'", '')


def validate_character(player, apikey, region="US", locale="en_US"):
    if region not in region_info:
        return None

    if locale not in region_info[region]['locales']:
        return None

    try:
        name, realm = player.split('-', 1)
        request_url = request_pattern.format(region_info[region]['api_url'], realm, name, locale, apikey)

        r = requests.get(request_url)

        if r.status_code != 200:
            return None

        data = r.json()

        if data['name'].lower() == name.lower() and get_realm_slug(data['realm']) == get_realm_slug(realm):
            return name, realm, region

        return None
    except KeyError:
        return None
