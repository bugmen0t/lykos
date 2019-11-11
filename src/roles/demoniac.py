import re
import random
import itertools
import math
from collections import defaultdict

from src.utilities import *
from src import channels, users, debuglog, errlog, plog
from src.functions import get_players, get_all_players, get_main_role, get_reveal_role, get_target
from src.decorators import command, event_listener
from src.containers import UserList, UserSet, UserDict, DefaultUserDict
from src.messages import messages
from src.status import try_misdirection, try_exchange

@event_listener("transition_night_end")
def on_transition_night_end(evt, var):
    for demoniac in get_all_players(("demoniac",)):
        if demoniac.prefers_simple():
            demoniac.send(messages["role_simple"].format("demoniac"))
        else:
            demoniac.send(messages["demoniac_notify"])

# monster is at priority 4, and we want demoniac to take precedence
@event_listener("chk_win", priority=4.1) # FIXME: Kill the priorities
def on_chk_win(evt, var, rolemap, mainroles, lpl, lwolves, lrealwolves):
    demoniacs = len(rolemap.get("demoniac", ()))
    traitors = len(rolemap.get("traitor", ()))
    cubs = len(rolemap.get("wolf cub", ()))

    if not lrealwolves and not traitors and not cubs and demoniacs:
        evt.data["message"] = messages["demoniac_win"].format(demoniacs)
        evt.data["winner"] = "demoniacs"

@event_listener("player_win")
def on_player_win(evt, var, player, role, winner, survived):
    if role == "demoniac" and winner == "demoniacs":
        evt.data["won"] = True

@event_listener("get_role_metadata")
def on_get_role_metadata(evt, var, kind):
    if kind == "role_categories":
        evt.data["demoniac"] = {"Neutral", "Win Stealer"}
