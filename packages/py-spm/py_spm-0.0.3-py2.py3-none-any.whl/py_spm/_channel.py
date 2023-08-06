from py_spm.utils import empty_to_none

chan_types = {
    "EOG": ["VEOG", "HEOG"],
    "ECG": ["EKG"],
    "REF": ["REFMAG", "REFGRAD", "REFPLANAR"],
    "MEG": ["MEGMAG", "MEGGRAD"],
    "MEGANY": ["MEG", "MEGMAG", "MEGGRAD", "MEGPLANAR"],
    "MEEG": ["EEG", "MEG", "MEGMAG", "MEGCOMB", "MEGGRAD", "MEGPLANAR"],
}


class Channel:
    def __init__(self, bad=None, label=None, type_=None, x=None, y=None, units=None):
        self.bad = bad
        self.label = label
        self.type = type_
        self.x = empty_to_none(x)
        self.y = empty_to_none(y)
        self.units = units

    @classmethod
    def from_dict(cls, channel_dict):
        if "X_plot2D" in channel_dict:
            channel_dict["x"] = channel_dict.pop("X_plot2D")
        if "Y_plot2D" in channel_dict:
            channel_dict["y"] = channel_dict.pop("Y_plot2D")

        return cls(
            bad=channel_dict.get("bad", None),
            label=channel_dict.get("label", None),
            type_=channel_dict.get("type", None),
            x=channel_dict.get("x", None),
            y=channel_dict.get("y", None),
            units=channel_dict.get("units", None),
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bad={self.bad}, "
            f"label='{self.label}', "
            f"type_='{self.type}', "
            f"x={self.x}, "
            f"y={self.y}, "
            f"units='{self.units}')"
        )
