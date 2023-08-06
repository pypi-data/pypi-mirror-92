from py_spm.utils import empty_to_zero


class Event:
    def __init__(self, type_, value, duration, time, offset):
        self.type = type_
        self.value = value
        self.duration = empty_to_zero(duration)

        if "artefact" in self.type.lower():
            self.duration *= 1000

        self.time = time
        self.offset = offset
        self.end_time = time + self.duration / 1000

        self.sample = -1
        self.end_sample = -1

        self.good_sample = -1
        self.good_end_sample = -1

        self.trial_start = -1
        self.trial_end = -1

    @classmethod
    def from_dict(cls, event_dict):
        if "type" in event_dict:
            event_dict["type_"] = event_dict.pop("type")
        return cls(**event_dict)

    def to_dict(self):
        return {
            "type_": self.type,
            "value": self.value,
            "duration": self.duration,
            "time": self.time,
            "offset": self.offset,
        }

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(type_='{self.type}', "
            f"value={self.value}, "
            f"duration={self.duration}, "
            f"time={self.time}, "
            f"offset={self.offset})"
        )
