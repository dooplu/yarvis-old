import winsdk.windows.media.capture as wdmc
import winsdk.windows.media.capture.frames as wdmcf
import winsdk.windows.devices.enumeration

frameSourceGroups = await wdmcf.MediaFrameSourceGroup.find_all_async()