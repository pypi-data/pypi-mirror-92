from dataclasses import dataclass

import numpy as np
from scipy.io import loadmat

from ._channel import Channel, chan_types
from ._data import Data
from ._trial import Trial
from .utils import check_lowered_string


class MEEG:
    def __init__(self, filename):
        D = loadmat(filename, simplify_cells=True)["D"]
        self.type = D["type"]
        self.n_samples = D["Nsamples"]
        self.f_sample = D["Fsample"]
        self.time_onset = D["timeOnset"]
        self.trials = Trial(**D["trials"])
        self.channels = [Channel.from_dict(channel) for channel in D["channels"]]
        self.data = Data(**D["data"])
        self.fname = D["fname"]
        self.path = D["path"]
        self.sensors = D["sensors"]
        self.fiducials = D["fiducials"]
        self.transform = D["transform"]
        self.condlist = D["condlist"]
        self.montage = D["montage"]
        self.history = D["history"]
        self.other = D["other"]

        self.trials.calculate_samples(self.f_sample)
        self.index = np.ones(self.n_samples, dtype=bool)
        self.good_index = np.zeros(self.n_samples, dtype=int)

        self.mark_artefacts_as_bad()
        self.reindex_good_samples()
        self.reindex_event_samples()

        self.trial_definition = None

    def epoch_data(self, data):
        trial_def = self.trial_definition
        if trial_def is None:
            raise ValueError("No trials has been defined.")

        trials = self.trials
        events = check_lowered_string(self.trials.types, trial_def.event_type)

        starts = np.round(trials.good_samples) - trial_def.pre_stim * self.f_sample
        starts = starts[events]

        ends = np.round(trials.good_end_samples) + trial_def.post_stim * self.f_sample
        ends = ends[events]

        valid = (starts > 0) & (ends < min(self.index.sum(), data.shape[0]))

        epochs = []
        for start, end in zip(starts[valid], ends[valid]):
            epochs.append(data[start:end])

        return np.array(epochs)

    def define_trial(self, event_type, pre_stim, post_stim):
        self.trial_definition = TrialParameters(event_type, pre_stim, post_stim)

    def mark_artefacts_as_bad(self):
        artefacts = check_lowered_string(self.trials.types, "artefact")
        starts = self.trials.samples[artefacts]
        ends = self.trials.end_samples[artefacts]

        for start, end in zip(starts, ends):
            self.index[start:end] = False

    def _channel_property(self, property_):
        return np.array([getattr(channel, property_) for channel in self.channels])

    def channel_types(self):
        return self._channel_property("type")

    def channel_selection(self, channel_type):
        return np.isin(self.channel_types(), chan_types[channel_type])

    def full_index(self, channel_type):
        return np.ix_(self.index, self.channel_selection(channel_type))

    def reindex_good_samples(self):
        self.good_index = np.zeros_like(self.index) - 1
        self.good_index[self.index] = np.arange(self.index.sum())
        self.good_index = np.minimum(self.good_index, self.n_samples)

    def reindex_event_samples(self):
        self.trials.good_samples = self.good_index[self.trials.samples]

        # TODO: Sort out this hacky solution to excess samples.
        #  It might actually not be hacky, bad segments *may* extend past n_samples.
        self.trials.good_end_samples = self.good_index[
            np.minimum(self.trials.end_samples, self.n_samples - 1)
        ]

    @property
    def n_good_samples(self):
        return self.index.sum()


@dataclass
class TrialParameters:
    event_type: str
    pre_stim: float
    post_stim: float
