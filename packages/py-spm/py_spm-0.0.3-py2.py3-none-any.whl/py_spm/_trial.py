from logging import getLogger

import numpy as np
from py_spm._event import Event

_logger = getLogger("py_spm")


class Trial:
    def __init__(self, label, events, onset, bad, tag, repl):
        self.label = label
        self.events = [Event.from_dict(event_dict) for event_dict in events]
        self.onset = onset
        self.bad = bad
        self.tag = tag
        self.repl = repl

    def calculate_samples(self, sample_frequency):
        for event in self.events:
            event.sample = np.floor(event.time * sample_frequency).astype(int)
            event.end_sample = np.floor(event.end_time * sample_frequency).astype(int)

    def _event_property(self, property_):
        return np.array([getattr(event, property_) for event in self.events])

    def _set_event_property(self, property_, values):
        if len(self.events) != len(values):
            _logger.warning(
                f"{len(self.events)} events, but {len(values)} values given."
            )
        for event, value in zip(self.events, values):
            setattr(event, property_, value)

    @property
    def types(self):
        return self._event_property("type")

    @property
    def values(self):
        return self._event_property("value")

    @property
    def durations(self):
        return self._event_property("duration")

    @property
    def times(self):
        return self._event_property("time")

    @property
    def offsets(self):
        return self._event_property("offset")

    @property
    def end_times(self):
        return self._event_property("end_time")

    @property
    def samples(self):
        return self._event_property("sample")

    @property
    def end_samples(self):
        return self._event_property("end_sample")

    @property
    def good_samples(self):
        return self._event_property("good_sample")

    @good_samples.setter
    def good_samples(self, values):
        self._set_event_property("good_sample", values)

    @property
    def good_end_samples(self):
        return self._event_property("good_end_sample")

    @good_end_samples.setter
    def good_end_samples(self, values):
        return self._set_event_property("good_end_sample", values)

    @property
    def trial_starts(self):
        return self._event_property("trial_start")

    @trial_starts.setter
    def trial_starts(self, values):
        return self._set_event_property("trial_start", values)
