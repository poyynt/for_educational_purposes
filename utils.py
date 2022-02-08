def get_cfg_from_script(script):
    import json
    script = script[script.find("M.cfg") + 8:]
    script = script[:script.find(";")]
    return json.loads(script)


def get_course_id_from_script(script):
    import json
    script = script[script.find("broker.init") + 12:]
    script = script[:script.find(";") - 1]
    return json.loads(script)["meetingid"]


def get_bn_id_from_script(script):
    import json
    script = script[script.find("broker.init") + 12:]
    script = script[:script.find(";") - 1]
    return json.loads(script)["bigbluebuttonbnid"]


def beep():
    from config import beep
    from time import sleep
    for _ in range(beep["count"]):
        print("\a")
        sleep(beep["delay"])
