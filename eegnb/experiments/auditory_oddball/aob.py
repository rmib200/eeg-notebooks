import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event, sound

from time import time
from eegnb.devices.eeg import EEG
from eegnb.experiments import Experiment


class AuditoryOddball(Experiment.BaseExperiment):
    
    def __init__(self, duration=120, eeg: EEG=None, save_fn=None, n_trials = 2010, iti = 0.3, soa = 0.2, jitter = 0.2, secs=0.2, volume=0.8, random_state=42, s1_freq="C", s2_freq="D", s1_octave=5, s2_octave=6):
        """

        Auditory Oddball Experiment
        ===========================

        Unique Parameters:
        -----------

        secs - duration of the sound in seconds (default 0.2)

        volume - volume of the sounds in [0,1] (default 0.8)

        random_state - random seed (default 42)

        s1_freq - frequency of first tone
        s2_freq - frequency of second tone

        s1_octave - octave of first tone
        s2_octave - octave of second tone

        """

        exp_name = "Auditory Oddball"
        super().__init__(exp_name, duration, eeg, save_fn, n_trials, iti, soa, jitter)
        self.secs = secs
        self.volume = volume
        self.random_state = random_state
        self.s1_freq = s1_freq
        self.s2_freq = s2_freq
        self.s1_octave = s1_octave
        self.s2_octave = s2_octave

    def load_stimulus(self):
        
        # Set up trial parameters
        np.random.seed(random_state)
        
        # Initialize stimuli
        aud1, aud2 = sound.Sound(s1_freq, octave=s1_octave, secs=secs), sound.Sound(s2_freq, octave=s2_octave, secs=secs)
        aud1.setVolume(volume)
        aud2.setVolume(volume)
        self.auds = [aud1, aud2]

        # Setup trial list
        sound_ind = np.random.binomial(1, 0.25, n_trials)
        itis = iti + np.random.rand(n_trials) * jitter
        self.trials = DataFrame(dict(sound_ind=sound_ind, iti=itis))
        self.trials["soa"] = soa
        self.trials["secs"] = secs

        self.fixation = visual.GratingStim(win=self.window, size=0.2, pos=[0, 0], sf=0, rgb=[1, 0, 0])
        self.fixation.setAutoDraw(True)
        self.window.flip()

        return 
    
    def present_stimulus(self, idx : int):
    
        # The wait time between trials differs might have to be an option that's hard coded 
        #    core.wait(trial["iti"])

        # itterrows iterates as series pair - might have to be tested since I am not passing trial
        trial = self.trials[idx]
        
        # Select and play sound
        ind = int(trial["sound_ind"])
        self.auds[ind].stop()
        self.auds[ind].play()

        # Push sample
        if self.eeg:
            timestamp = time()
            marker = [self.markernames[ind]]
            marker = list(map(int, marker))
            self.eeg.push_sample(marker=marker, timestamp=timestamp)


