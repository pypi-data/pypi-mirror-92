import requests

from juna.types import GameMode, Skill, Activity, SkillInfo, ActivityInfo

HISCORES_URL_TEMPLATE = (
    "https://secure.runescape.com/m={module}/index_lite.ws?player={player}"
)


def hiscores_module_name(game_mode: GameMode) -> str:
    if game_mode == GameMode.RUNESCAPE_REGULAR:
        return "hiscore"
    elif game_mode == GameMode.RUNESCAPE_IRONMAN:
        return "hiscore_ironman"
    elif game_mode == GameMode.RUNESCAPE_HARDCORE_IRONMAN:
        return "hiscore_hardcore_ironman"
    elif game_mode == GameMode.OLDSCHOOL_REGULAR:
        return "hiscore_oldschool"
    elif game_mode == GameMode.OLDSCHOOL_IRONMAN:
        return "hiscore_oldschool_ironman"
    elif game_mode == GameMode.OLDSCHOOL_HARDCORE_IRONMAN:
        return "hiscore_oldschool_hardcore_ironman"
    elif game_mode == GameMode.OLDSCHOOL_ULTIMATE_IRONMAN:
        return "hiscore_oldschool_ultimate_ironman"
    elif game_mode == GameMode.OLDSCHOOL_DEADMAN:
        return "hiscore_oldschool_deadman"


def hiscores_url(display_name: str, game_mode: GameMode):
    module_name = hiscores_module_name(game_mode)
    return HISCORES_URL_TEMPLATE.format(module=module_name, player=display_name)


def process_hiscores_line(line: str):
    parts = line.split(",")
    if len(parts) == 3:
        return SkillInfo(*parts)
    elif len(parts) == 2:
        return ActivityInfo(*parts)


def process_hiscores_data(data: str, game_mode: GameMode):
    if game_mode in GameMode.modern_modes():
        skills = Skill.modern_skills()
        activities = Activity.modern_activities()
    else:
        skills = Skill.oldschool_activities()
        activities = Activity.oldschool_activities()

    stats = skills + activities
    lines = data.splitlines()

    return dict(zip(stats, [process_hiscores_line(line) for line in lines]))


def load(display_name: str, game_mode: GameMode):
    url = hiscores_url(display_name, game_mode)
    res = requests.get(url)

    if res.status_code == 200:
        return process_hiscores_data(res.text, game_mode)
    else:
        raise ValueError(f"Hiscores not found for {display_name}.")
