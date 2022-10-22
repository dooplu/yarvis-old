import asyncio
import winsdk.windows.media.capture as wdmc
import winsdk.windows.media.capture.frames as wdmcf
import winsdk.windows.devices.enumeration

async def getCameras():
    frameSourceGroups = await wdmcf.MediaFrameSourceGroup.find_all_async()
    return frameSourceGroups

frameSourceGroups = asyncio.get_event_loop().run_until_complete(getCameras())
 


for currentSourceGroup in frameSourceGroups:
    for sourceInfo in currentSourceGroup.source_infos:
        if sourceInfo.media_stream_type == 0:
            if sourceInfo.source_kind == wdmcf.MediaFrameSourceInfo.source_kind.COLOR:
                break

selectedGroup = currentSourceGroup
colorSourceInfo = sourceInfo
#print(selectedGroup)

mediaCapture = wdmc.MediaCapture()
settings = wdmc.MediaCaptureInitializationSettings()
settings.source_group = selectedGroup
settings.sharing_mode = wdmc.MediaCaptureSharingMode.EXCLUSIVE_CONTROL
settings.memory_preference = wdmc.MediaCaptureMemoryPreference.CPU
settings.streaming_capture_mode = wdmc.StreamingCaptureMode.VIDEO

try:
    mediaCapture.initialize_async(settings)
except:
    print("failed to initialize mediacapture")