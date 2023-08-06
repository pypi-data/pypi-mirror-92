import librosa
import numpy as np


def get_beats(file, print_infos=False):
    if print_infos:
        print('get_beats load:', file)
    y, sr = librosa.load(file)
    # print(y, sr)
    # tempo, beat_times = librosa.beat.beat_track(y=y, sr=sr, units='time')
    # 使用预先计算的起始包络跟踪节拍
    onset_env = librosa.onset.onset_strength(y, sr=sr, aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    # print(beats)
    beat_times = list(librosa.frames_to_time(beats, sr=sr))
    # beat_times.append(beat_times[-1] + 1)  # 最后一位重复了一下，并往后偏移1秒
    if print_infos:
        print('get_beats return：', onset_env, sr, beats, beat_times)
    return onset_env, sr, beats, beat_times
