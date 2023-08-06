"""
https://github.com/Breakthrough/PySceneDetect
scenedetect[opencv,progress_bar]
"""

import os
import csv
import json

import cv2
from ilds.time import Timer
from moviepy.editor import *
# 用于以帧精确度对时间码进行存储，转换和执行算术的类
from scenedetect.frame_timecode import FrameTimecode
# 标准 PySceneDetect 导入
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
# 用于缓存检测指标并保存/加载到统计文件
from scenedetect.stats_manager import StatsManager
# 检测视频内容的快速更改/剪辑
from scenedetect.detectors.content_detector import ContentDetector
# 检测视频亮度/强度的变化
from scenedetect.detectors.threshold_detector import ThresholdDetector
# https://pyscenedetect-manual.readthedocs.io/en/latest/api/video_splitter.html
from scenedetect import video_splitter

# 场景标题
SCENE_HEADER = ['start', 'end', 'fps']
# 场景标记标题
SCENE_MARKER_HEADER = ['text', 'time']
# 场景文件保存的文件夹
SCENE_DIR = '@seDir'


def get_scene_dir(file, is_make=False):
    """
    获取场景相关文件保存目录

    我们把场景相关的文件保存到视频文件当前目录\SCENE_DIR\视频文件(包含后缀)\文件保存到这儿

    :return: 当前文件的场景目录
    """

    file_dir, file_name = os.path.split(file)

    scene_dir = os.path.join(file_dir, SCENE_DIR, file_name)

    if is_make and not os.path.exists(scene_dir):
        os.makedirs(scene_dir)

    return scene_dir


def get_scene_list(video_path):
    """获取场景列表"""
    # 创建一个 video_manager 指向视频文件
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)

    # 添加 ContentDetector 算法（构造函数采用阈值等检测器选项）
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    # 设置缩减系数以提高处理速度。
    video_manager.set_downscale_factor()

    # 启动 video_manager.
    video_manager.start()

    # 在 video_manager 上执行场景检测
    scene_manager.detect_scenes(frame_source=video_manager)

    # 返回每个检测到的场景的开始/结束 FrameTimecode 元组列表
    scene_list = scene_manager.get_scene_list(base_timecode)

    video_manager.release()

    return scene_list


def load_scene_list(csv_file, encoding='utf-8-sig'):
    """
    从 csv 文件读取场景时间
    """
    scene_list = []
    # 读取csv文件
    with open(csv_file, newline='', encoding=encoding) as f:
        reader = csv.reader(f)  # delimiter=':', quoting=csv.QUOTE_NONE

        iter_reader = iter(reader)
        header = next(iter_reader)  # fieldnames

        # print(header)
        if header != SCENE_HEADER:
            raise ValueError(f'文件头验证失败, {header},{SCENE_HEADER}')

        try:
            for row in iter_reader:
                # print(row)
                # 每个场景都是 (start, end) FrameTimecode 元组
                fps = float(row[2])
                scene_list.append((FrameTimecode(row[0], fps), FrameTimecode(row[1], fps)))
        except csv.Error as e:
            raise ValueError(f'file {csv_file}, line {reader.line_num}: {e}')
        # else:
        #     print('读取完成')
    return scene_list


def save_scene_list(scene_list, csv_file, encoding='utf-8-sig'):
    """
    保存场景时间到 csv 文件
    """
    # 写入csv文件
    with open(csv_file, 'w', newline='', encoding=encoding) as f:
        writer = csv.writer(f)
        writer.writerow(SCENE_HEADER)
        for i, scene in enumerate(scene_list):
            # print(scene[0].get_frames(), scene[0].get_framerate(), scene[0].get_timecode(), scene[1].get_frames(),
            #       scene[1].get_framerate(), scene[1].get_timecode())
            # 写入单行
            writer.writerow([scene[0].get_frames(), scene[1].get_frames(), scene[0].get_framerate()])


def save_scene_marker(scene_list, csv_file, encoding='utf-8-sig'):
    """
    保存为场景标记
    """
    # 写入csv文件
    with open(csv_file, 'w', newline='', encoding=encoding) as f:
        writer = csv.writer(f)
        writer.writerow(SCENE_MARKER_HEADER)
        for i, scene in enumerate(scene_list):
            # print(scene[0].get_frames(), scene[0].get_framerate(), scene[0].get_timecode(), scene[1].get_frames(),
            #       scene[1].get_framerate(), scene[1].get_timecode())
            # 写入单行
            writer.writerow([scene[1].get_timecode(), scene[1].get_seconds()])


@Timer.time_it
def find_scenes(video_path, is_update=False, print_infos=False, to_scene_dir=None, scene_name=None, stats_name=None,
                info_name=None):
    # type: (str, bool) -> List[Tuple[FrameTimecode, FrameTimecode]]
    """
    查找场景信息

    :param video_path: 视频文件路径
    :param is_update: 是否更新已有的 stats
    :param print_infos: 打印信息
    :param to_scene_dir: 场景文件保存的目录
    :param scene_name: 场景名字
    :param stats_name: stats名字
    :param info_name: 视频信息文件名
    :return:
    """

    print('find_scenes:', video_path)

    if to_scene_dir is None:
        scene_dir = get_scene_dir(video_path, is_make=True)
    elif isinstance(to_scene_dir, str):
        scene_dir = to_scene_dir
    elif callable(to_scene_dir):
        scene_dir = to_scene_dir(video_path)
    else:
        scene_dir = to_scene_dir

    if not os.path.exists(scene_dir):
        os.makedirs(scene_dir, exist_ok=True)

    if scene_name is None:
        scene_name = 'scene.csv'

    if stats_name is None:
        stats_name = 'stats.csv'

    if info_name is None:
        info_name = 'info.json'

    # 场景列表保存到 scene_dir\scene.csv
    scene_file_path = os.path.join(scene_dir, scene_name)
    # 我们直接检查是否有场景文件，如果已经存在，且不需要更新的时候直接读取
    if os.path.exists(scene_file_path) and not is_update:
        return load_scene_list(scene_file_path)

    # 统计文件保存到 scene_dir\stats.csv
    stats_file_path = os.path.join(scene_dir, stats_name)

    # VideoManager 的 video_files 参数是要打开的视频文件列表。可以追加任意数量的视频，但是，每个视频必须具有相同的帧速率和分辨率
    # 如果视频帧率略有不同，请提供 framerate 参数以覆盖帧率检查
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    # 构造我们的 SceneManager 并将其传递给我们的 StatsManager
    scene_manager = SceneManager(stats_manager)

    # 添加 ContentDetector 算法（每个检测器的构造函数采用检测器选项，例如阈值）
    scene_manager.add_detector(ContentDetector())
    # 添加 ThresholdDetector 算法（）
    # scene_manager.add_detector(ThresholdDetector())
    # 获取基本的 FrameTimecode
    base_timecode = video_manager.get_base_timecode()

    # 保存视频文件信息
    try:
        width, height = video_manager.get_framesize()
        framerate = video_manager.get_framerate()
        duration = (base_timecode + video_manager._frame_length).get_seconds()
        # print(duration, width, height, framerate)
        info = {
            'file_name': os.path.basename(video_path),
            'width': width,
            'height': height,
            'framerate': framerate,
            'duration': duration,
        }
        info_file = os.path.join(scene_dir, info_name)
        # from ilds.json import json_save
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('保存视频文件信息失败 ', video_path, e)

    # 据视频分辨率将持续时间设置为2分钟
    # video_manager.set_duration(duration=base_timecode + '00:02:00')

    scene_list = []

    try:
        # 如果 stats 文件存在，请加载它。
        if os.path.exists(stats_file_path):
            # 从以读取模式打开的 CSV 文件中读取统计信息
            with open(stats_file_path, 'r') as stats_file:
                stats_manager.load_from_csv(stats_file, base_timecode)

        # 设置缩小因子以提高处理速度
        video_manager.set_downscale_factor()

        # 启动 video_manager
        video_manager.start()

        # while True:
        #     ret_val, frame_image = video_manager.read()
        #     if not ret_val:
        #         break
        #     # 在这里用frame_image做一些事情。

        # 在 video_manager 上进行场景检测
        scene_manager.detect_scenes(frame_source=video_manager)

        if print_infos:
            print('获取当前时间码', video_manager.get_current_timecode())
            print('获取持续时间', video_manager.get_duration())
            print('获取帧速率', video_manager.get_framerate())
            print('获取帧大小', video_manager.get_framesize())
            print('获取帧大小', video_manager.get_framesize_effective())
            print('获取视频数量', video_manager.get_num_videos())
            print('获取视频路径', video_manager.get_video_paths())

        # 获取检测到的场景列表
        scene_list = scene_manager.get_scene_list(base_timecode)
        # 每个场景都是 (start, end) FrameTimecodes 的元组

        if print_infos:
            print('获得的场景列表:')
            for i, scene in enumerate(scene_list):
                print(
                    '\tScene %2d: Start %s / Frame %d, End %s / Frame %d' % (
                        i + 1,
                        scene[0].get_timecode(), scene[0].get_frames(),
                        scene[1].get_timecode(), scene[1].get_frames(),))

        # 我们仅在需要保存时才写入stats文件
        if stats_manager.is_save_required():
            with open(stats_file_path, 'w') as stats_file:
                stats_manager.save_to_csv(stats_file, base_timecode)

    finally:
        # 确保即使在添加到过程框架的任何代码中引发异常时，也会调用 release()，清理 VideoManager 对象获取的所有资源
        video_manager.release()

    if scene_list:
        save_scene_list(scene_list, scene_file_path, encoding='utf-8-sig')

    return scene_list


def build_scenes(video_path):
    # 定义 re_scene_list 为视频切分场景的列表结果
    re_scene_list = []
    cap = cv2.VideoCapture(video_path)

    # 获取检测到的场景列表
    scene_list = get_scene_list(video_path)
    # 与 FrameTimecodes 一样，如果是，则可以对 scene_list 中的每个场景进行排序
    # 场景列表变为未排序。

    print('List of scenes obtained:')
    # print(scene_list)
    # 如果 scene_list 不为空，整理结果列表，否则，视频为单场景
    if scene_list:
        for i, scene in enumerate(scene_list):
            # print('%d , %d' % (scene[0].get_frames(), scene[1].get_frames()))
            re_scene = (scene[0].get_frames(), scene[1].get_frames())
            re_scene_list.append(re_scene)
    else:
        frames_num = cap.get(7)
        re_scene = (0, frames_num)
        re_scene_list.append(re_scene)
    # 输出切分场景的列表结果
    print(re_scene_list)

    return re_scene_list


@Timer.time_it
def moviepy_split_video(file, scene_list, out_dir=None, is_thumbnail=False, thumbnail_width=320, thumbnail_height=None,
                        interval=30, bitrate='700k', is_update=False):
    """
    按场景分割视频

    :param file: 要分割的视频文件
    :param scene_list: 场景列表，每个场景都是 (start, end) FrameTimecode 元组
    :param out_dir: 分割文件保存的目录，如果为空，我也放到默认文件夹： scene_dir\\split
    :param is_thumbnail: 是否缩放视频，如果原视频比要缩放的分辨率低，也不会缩放视频
    :param thumbnail_width: 视频缩放的宽度
    :param thumbnail_height: 视频缩放的高度，现在还没有使用
    :param interval: 分割视频的最小间隔，小于它的时候不分割
    :param bitrate: 保存压缩视频的码率
    :param is_update: 如果输出文件夹已经存在是否直接跳过
    :return: None
    """

    if out_dir is None:
        out_dir = os.path.join(get_scene_dir(file, is_make=False), 'split')
    elif callable(out_dir):
        out_dir = out_dir(file)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    elif not is_update:
        print('分割文件夹已经存在，跳过视频分割', file)
        return

    print('分割视频保存到：', out_dir)
    start = None
    clip = VideoFileClip(file)
    for i, scene in enumerate(scene_list):
        if start is None:
            start = scene[0].get_seconds()
        end = scene[1].get_seconds()

        if interval and end - start <= interval:
            continue

        # print(start, end, i, scene)
        subclip = clip.subclip(start, end)
        # subclip.write_videofile(os.path.join(out_dir, f'{i}.mp4'), codec='libx264', bitrate='3000k')
        if is_thumbnail and subclip.w > thumbnail_width:
            # print(subclip.h, subclip.w)
            # 因为缩放分辨率会有 Windows 不支持的情况，暂时先不缩放分辨率
            # subclip = subclip.resize((thumbnail_width, int(thumbnail_width * (subclip.h / subclip.w))))
            subclip = subclip.resize(width=thumbnail_width)
            subclip.write_videofile(os.path.join(out_dir, f'{start}.mp4'), codec='libx264', bitrate=bitrate)
        else:
            subclip.write_videofile(os.path.join(out_dir, f'{start}.mp4'))
        # 适合用于网络视频（使用HTML5），这个压缩慢五分之一左右，预览有时候不是第一帧
        # subclip.write_videofile(os.path.join(out_dir, f'{i}.webm'), codec='libvpx')
        start = None
