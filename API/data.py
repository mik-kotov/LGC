from itertools import cycle
from random import choice

headers = {
    "X-Trace-Id": "216fff40-98d9-41e3-a5e2-0800200c9a66",
    "Content-Type": "application/json",
    "X-App-Version": "1.2.0",
    "X-User-Platform": "ios",
    "X-User-DeviceId": "216fff40-98d9-41e3-a5e2-0800200c9a66",
    "X-Source": "LGC"
}

loymax_login = "m.kotov"
loymax_password = "QLEp38z5_6)7"

users_who_have_bonuses = [
    ["79251159333", "7780004731412369015"]
    # ["79636635097", "7780004785406095572"],
    # ["79213080302", "7780004771571411059"],
    # ["79652053091", "7780004799515350679"],
    # ["79301860006", "7780004158007374241"],
    # ["79213695955", "7780004736948414847"],
    # ["79057117022", "7780004782843446211"],
    # ["79150104010", "7785419379900162934"],
    # ["79601616888", "7785451494500125211"]
]
users_who_have_not_bonuses = ["79175518104"
                              "79163354447",
                              "79026166502",
                              "79609344999",
                              "79211387112",
                              "79673686932",
                              "79276932325"]

cities = [
    "6100000100000",
    "5500000100000",
    "6300000100000",
    "7400000100000",
    "7400000100000",
    "1600000100000",
    "6600000100000",
    "5400000100000",
    "7700000000000"
]

users_with_card_cycle = cycle(users_who_have_bonuses)
users_no_card_cycle = cycle(users_who_have_not_bonuses)

def get_random_city():
    return choice(cities)

def get_random_user_with_card():
    return choice(users_who_have_bonuses)


def get_random_user_with_no_card():
    return choice(users_who_have_not_bonuses)






