from collections import OrderedDict

try:
    import opentimelineio as otio
except ModuleNotFoundError:
    import opentimelineio_py as otio


def second_to_time_str(seconds):
    """
    秒转换为人类阅读的时间显示，用来显示已用时间
    例如：'1小时1分1.099秒'
    """
    time_str = ''
    hour = '%01d小时' % (seconds / 3600)
    minute = '%01d分' % ((seconds % 3600) / 60)

    if hour != '0小时':
        time_str += hour

    if minute != '0分':
        time_str += minute

    # seconds
    time_str += '%01d.%03d秒' % (seconds % 60, (seconds % 1) * 1000)

    return time_str


def summarize_range(label, time_range):
    if time_range is None:
        print("\t{}: None".format(label))
    else:
        print(
            "\t{}: {} - {} (Duration: {})".format(
                label,
                otio.opentime.to_timecode(
                    time_range.start_time
                ),
                otio.opentime.to_timecode(
                    time_range.end_time_exclusive()
                ),
                otio.opentime.to_timecode(time_range.duration)
            )
        )


def clip_range_info(clip, track_kind=''):
    print(f"Clip {track_kind}: {clip.name}")
    # 请参阅文档，以了解这些范围之间的区别：
    # https://opentimelineio.readthedocs.io/en/latest/tutorials/time-ranges.html
    summarize_range("Trimmed Range  （修剪范围）", clip.trimmed_range())  # 如果有 source_range，会使用她
    summarize_range("Visible Range  （可见范围）", clip.visible_range())
    summarize_range("Available Range（可用范围）", clip.available_range())


timeline_metadata = {'fcp_xml': OrderedDict([
    ('media',
     OrderedDict([
         ('video',
          OrderedDict([('format',
                        OrderedDict([('samplecharacteristics',
                                      OrderedDict([
                                          # 时间线的宽度和高度
                                          ('width', '1080'),
                                          ('height', '1920'),
                                          # pixelaspectratio 会影响到片段是否 等比缩放
                                          ('pixelaspectratio', 'square'),
                                      ]))]))])),
     ]))
]
)}

fcp_filter = OrderedDict([('effect',
                           OrderedDict([('name', 'Basic Motion'),
                                        ('effectid', 'basic'),
                                        ('effectcategory', 'motion'),
                                        ('effecttype', 'motion'),
                                        ('mediatype', 'video'),
                                        ('pproBypass', 'false'),
                                        ('parameter', [])
                                        ])
                           )]
                         )

# 缩放，不是等比缩放的时候，这个是缩放宽度
fcp_scale_effect = OrderedDict([('@authoringApp',
                                 'PremierePro'),
                                ('parameterid', 'scale'),
                                ('name', 'Scale'),
                                ('valuemin', '0'),
                                ('valuemax', '1000'),
                                ('value', '100')])
