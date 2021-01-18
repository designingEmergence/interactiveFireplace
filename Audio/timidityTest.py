from timidity import Parser, play_notes
import numpy as np

ps = Parser("MidiNotes/c-4.mid")

play_notes(*ps.parse(), np.sin)

#CONVERT SOUND TO SIN WAVE BEFORE PLAYING