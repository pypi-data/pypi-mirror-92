from opentrons.config import advanced_settings as advs


def short_fixed_trash():
    return advs.get_setting_with_env_overload('shortFixedTrash')


def calibrate_to_bottom():
    return advs.get_setting_with_env_overload('calibrateToBottom')


def dots_deck_type():
    return advs.get_setting_with_env_overload('deckCalibrationDots')


def disable_home_on_boot():
    return advs.get_setting_with_env_overload('disableHomeOnBoot')


def use_protocol_api_v2():
    return not advs.get_setting_with_env_overload('useLegacyInternals')


def use_old_aspiration_functions():
    return advs.get_setting_with_env_overload('useOldAspirationFunctions')


def enable_door_safety_switch():
    return advs.get_setting_with_env_overload('enableDoorSafetySwitch')


def enable_http_protocol_sessions():
    return advs.get_setting_with_env_overload('enableHttpProtocolSessions')
