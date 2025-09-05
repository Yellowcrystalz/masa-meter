"""
"""

import io
from pathlib import Path

from discord.ext import songbird


def load_track(path: Path, volume: float) -> songbird.Track:
    """Load audio file into a Songbird Track to be played.

    Args:
        path: A Path object pointing to audio file path.
        volume: A float representing how loud the track is to be played.

    Returns
        A Sonbird Track class with the audio file as its source.
    """

    with open(path, "rb") as audio:
        sine: io.BytesIO = io.BytesIO(audio.read())

    source = songbird.RawBufferSource(sine)
    track = songbird.Track(source).set_volume(volume)

    return track
