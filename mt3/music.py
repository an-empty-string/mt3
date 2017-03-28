import copy
import mido
import threading
import time
from . import lisp, evaluator

def play(env, out, notes):
    spb = 60 / env["_music_tempo"]
    t = spb * env["_music_ts"][1]

    for notel in notes:
        if not isinstance(notel[0], list):
            notel = [notel]

        print(notel)

        notel = [(note[0], t * note[1][0] / note[1][1]) for note in notel]
        notel.sort(key=lambda note: note[1])

        for note in notel:
            if note[0] > 127:
                time.sleep(note[1])
                continue
            print("on ", note)
            out.send(mido.Message('note_on', note=note[0], velocity=100))

        tt = 0
        for idx, note in enumerate(notel):
            if note[0] > 127:
                continue
            print("off", note)
            time.sleep(note[1] - tt)
            out.send(mido.Message('note_off', note=note[0]))
            tt += note[1]

def clocksetup(env, tempo, ts):
    env["_music_tempo"] = tempo
    env["_music_ts"] = ts
    env["_music_on_measure"] = []

def _clockstart(env):
    beats_per_minute = env["_music_tempo"]
    beats_per_measure = env["_music_ts"][0]
    seconds_per_beat = 60 / beats_per_minute
    n = 0

    while True:
        # tick
        for thing in env["_music_on_measure"]:
            print("run: ", [thing, n])
            threading.Thread(target=evaluator.evaluate, args=([thing, n], env)).start()
        n += 1
        time.sleep(seconds_per_beat * beats_per_measure)

def clockstart(env):
    t = threading.Thread(target=_clockstart, args=(env,))
    t.start()
    t.join()

def ontick(env, f):
    env["_music_on_measure"].append(f)

def music_env(out, env):
    env.update({
        'play': lambda e, notes: threading.Thread(target=play, args=(e, out, notes)).start(),
        'playf': lambda e, notes: play(e, out, notes),
        'clocksetup': clocksetup,
        'clockstart': clockstart,
        'ontick': ontick,
        'panic': lambda e: out.panic()
    })
    evaluator.run_file("mt3/music.mt3", env)
    return env
