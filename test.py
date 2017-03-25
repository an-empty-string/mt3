import copy
import mido
from mt3 import lisp, evaluator, music

env = copy.copy(evaluator.default_env)
evaluator.run_file("mt3/env.mt3", env)
music.music_env(mido.open_output('Synth input port (qsynth:0)'), env)
evaluator.run_file("test.mt3", env)
