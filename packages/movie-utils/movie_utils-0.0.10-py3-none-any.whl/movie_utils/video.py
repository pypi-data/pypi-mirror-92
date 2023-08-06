import os
import copy

# ffmpeg 下载
# https://ffmpeg.zeranoe.com/builds/
# https://github.com/Zulko/moviepy
# pip install moviepy  # https://zulko.github.io/moviepy/install.html
from moviepy.editor import AudioFileClip, VideoFileClip  # , TextClip, CompositeVideoClip

# https://github.com/PixarAnimationStudios/OpenTimelineIO
try:
    import opentimelineio as otio
except ModuleNotFoundError:
    import opentimelineio_py as otio

from .utils import clip_range_info
from .utils import timeline_metadata
from .utils import fcp_filter, fcp_scale_effect
from .scene_detect import find_scenes

AUDIO_EXTS = {'.wav', '.aac', '.mp3', '.aif', '.aiff', '.m4a'}
VIDEO_EXTS = {'.mp4', }
IMAGE_EXTS = {'.jpg', '.png', '.psd', }


def rational_time(seconds, fps):
    """
    转换为 opentimelineio 的时间
    """
    # RationalTime(value=0.0, rate=1.0) 用秒来表示时间，
    # 1秒 = value * (1/rate) ，我们需要 rescaled_to(fps) 到实际时间
    return otio.opentime.RationalTime(seconds, 1.0).rescaled_to(fps)


def create_scene_clips(scene_list, name, media, fps):
    """
    创建场景剪辑
    """
    scene_clips = []
    for i, scene in enumerate(scene_list):
        # fcp 需要 source_range
        source_range = otio.opentime.range_from_start_end_time(rational_time(scene[0].get_seconds(), fps),
                                                               rational_time(scene[1].get_seconds(), fps))
        clip = otio.schema.Clip(name=f"{name} 场景 {i}".strip(), media_reference=media, source_range=source_range)
        scene_clips.append(clip)
    return scene_clips


class Timeline(otio.schema.Timeline):

    def __init__(self, name='时间线', tracks=None, global_start_time=None, metadata=None):
        super().__init__(name, tracks, global_start_time, metadata)
        self.debug = True
        self.media_library = {}
        self.media = None
        self.clip = None
        self.fps = None

        # 在时间线添加视频轨道
        self.tracks.append(otio.schema.Track(name='视频 1', kind=otio.schema.TrackKind.Video, ))
        self.tracks.append(otio.schema.Track(name='视频 2', kind=otio.schema.TrackKind.Video, ))
        self.tracks.append(otio.schema.Track(name='视频 3', kind=otio.schema.TrackKind.Video, ))
        # 在时间线添加音频轨道
        self.tracks.append(otio.schema.Track(name='音频 1', kind=otio.schema.TrackKind.Audio, ))
        self.tracks.append(otio.schema.Track(name='音频 2', kind=otio.schema.TrackKind.Audio, ))
        self.tracks.append(otio.schema.Track(name='音频 3', kind=otio.schema.TrackKind.Audio, ))

    def add_media(self, file_path):
        """添加媒体"""
        if file_path in self.media_library:
            self.media = self.media_library[file_path]
            if self.debug:
                print('文件已经存在', file_path)
            return self.media

        file_ext = os.path.splitext(file_path)[-1].lower()
        clip = None
        if file_ext in AUDIO_EXTS:
            clip = AudioFileClip(file_path)
            fps = 1
            end = clip.end
            # 保存一些剪辑的属性
            metadata = {
                'file_path': clip.filename,
                'duration': clip.duration,
                'end': end,
                'fps': fps,
            }
        elif file_ext in VIDEO_EXTS:
            clip = VideoFileClip(file_path)
            fps = clip.fps
            end = clip.end
            # 保存一些剪辑的属性
            metadata = {
                'file_path': clip.filename,
                'duration': clip.duration,
                'end': end,
                'fps': fps,
                'size': clip.size,
                'rotation': clip.rotation,
            }
        elif file_ext in IMAGE_EXTS:
            fps = 1
            end = 30
            # 保存一些剪辑的属性
            metadata = {
                'file_path': file_path,
                'duration': 1,
                'end': 1,
                'fps': fps,
            }
        else:
            raise ValueError(f'没有添加支持的媒体文件 {file_path}')
        if clip:
            clip.close()
        # clip = FFProbe(file_path)

        # fps = _ffprobe_fps(os.path.basename(file_path), file_path, dryrun=False)
        # _available_range = _media_start_end_of(file_path, fps)
        # print('比较两种不同方法获取的数据', fps, _available_range, available_range)

        if self.fps is None:
            self.fps = fps
        available_range = otio.opentime.TimeRange(rational_time(0, fps), rational_time(end, fps))
        if self.debug:
            print(end, self.fps, available_range)
        # 通过URL引用媒体
        media_reference = otio.schema.ExternalReference(
            target_url="file://localhost/" + file_path,
            available_range=available_range,  # 可用范围，也是必须要的
        )
        media_reference.metadata = metadata
        if self.debug:
            print(metadata)

        self.media_library[file_path] = media_reference
        # print(media_reference.available_range.start_time.rate)
        self.media = media_reference
        return media_reference

    def get_media_fps(self, media=None):
        if isinstance(media, otio.schema.ExternalReference):
            return media.available_range.start_time.rate
        elif self.media:
            return self.media.available_range.start_time.rate
        else:
            raise ValueError('没有选择媒体文件')

    def add_clip(self, media=None, name='', source_range=None, video_track=0, audio_track=3):
        """添加剪辑"""
        if isinstance(media, otio.schema.ExternalReference):
            self.media = media

        if self.media is None:
            raise ValueError('请从 media_library 中选择媒体')

        if source_range is None:
            source_range = self.media.available_range

        if not name:
            name = os.path.basename(self.media.target_url)

        clip = None

        if audio_track is not None:
            clip = otio.schema.Clip(name=name, media_reference=self.media, source_range=source_range)
            self.tracks[audio_track].append(clip)
            if self.debug:
                clip_range_info(clip, 'Audio')

        if video_track is not None:
            # fcp 需要 source_range
            clip = otio.schema.Clip(name=name, media_reference=self.media, source_range=source_range)
            self.tracks[video_track].append(clip)
            if self.debug:
                clip_range_info(clip, 'Video')

        # 如果有添加视频轨道，我们使用视频的，如果没有那么我们使用音频的
        self.clip = clip

        return clip

    def add_scene_segmentation(self, name='', video_track=1, audio_track=4):
        """添加场景分割"""
        if self.media is None:
            raise ValueError('请从 media_library 中选择媒体')

        if not name:
            name = os.path.basename(self.media.target_url)
        scene_clips = []

        file_path = self.media.metadata['file_path']
        scene_list = find_scenes(file_path)
        # print(len(scenes), scenes)
        if not scene_list:
            clip = self.add_clip(name=name, source_range=None, video_track=video_track, audio_track=audio_track)
            return [clip]
        fps = self.get_media_fps(media=None)

        if video_track is not None:
            scene_clips = create_scene_clips(scene_list, name, self.media, fps)
            self.tracks[video_track].extend(scene_clips)

        if audio_track is not None:
            self.tracks[audio_track].extend(create_scene_clips(scene_list, name, self.media, fps))

        return scene_clips

    def add_gap(self, name='', duration=1.0, fps=None, video_track=0, audio_track=None):
        if fps is None:
            fps = self.fps
        # 我们不能指定剪辑位置，只能用空白填充位置
        # 将 source_range 设置为空 ，设置持续时间（duration） TimeRange ，以方便创建一定长度的间隙
        if isinstance(video_track, int):
            self.tracks[video_track].append(otio.schema.Gap(name, duration=rational_time(duration, fps)))

        if isinstance(audio_track, int):
            self.tracks[audio_track].append(otio.schema.Gap(name, duration=rational_time(duration, fps)))

    def write_to_file(self, filepath, adapter_name=None):
        """
        写入到文件

        :param filepath: 保存文件
        :param adapter_name: fcp_xml, otio_json, cmx_3600, fcpx_xml
        :return:
        """
        if self.debug:
            print(f'write_to_file: {filepath}')
        otio.adapters.write_to_file(self, filepath, adapter_name=adapter_name)


class PremiereTimeline(Timeline):
    def __init__(self, name='时间线', tracks=None, global_start_time=None, metadata=None):
        super().__init__(name, tracks, global_start_time, metadata)
        # 保存的时候再添加效果到剪辑中
        self.clip_effects = {}
        self.metadata.update(timeline_metadata)
        self._width = self.metadata['fcp_xml']['media']['video']['format']['samplecharacteristics']['width']
        self._height = self.metadata['fcp_xml']['media']['video']['format']['samplecharacteristics']['height']
        # print(self.width, self.height)

    @property
    def width(self):
        """
        获取时间线宽
        """
        return self._width

    @width.setter
    def width(self, v):
        """
        设置时间线宽
        """
        self._width = v
        self.metadata['fcp_xml']['media']['video']['format']['samplecharacteristics']['width'] = v

    @property
    def height(self):
        """
        获取时间线高
        """
        return self._height

    @height.setter
    def height(self, v):
        """
        设置时间线高
        """
        self._height = v
        self.metadata['fcp_xml']['media']['video']['format']['samplecharacteristics']['height'] = v

    def set_clip_effect(self, clip, effect, data):
        clip.metadata['fcp_xml'] = {'filter': []}
        self.clip_effects[clip] = {effect: data}

    def write_to_file(self, filepath):
        """
        写入到文件
        """
        # 添加设置的效果到剪辑中
        for clip, effect_data in self.clip_effects.items():
            clip_filter = copy.deepcopy(fcp_filter)
            for effect, data in effect_data.items():
                if effect == 'scale':
                    scale_effect = copy.deepcopy(fcp_scale_effect)
                    scale_effect.update(data)
                    clip_filter['effect']['parameter'].append(scale_effect)
                else:
                    raise ValueError(f'不支持的效果：{effect}:data')
            clip.metadata['fcp_xml']['filter'].append(clip_filter)

        super().write_to_file(filepath)
