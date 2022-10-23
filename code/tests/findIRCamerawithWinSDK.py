import asyncio
import winsdk.windows.media.capture as wdmc
import winsdk.windows.media.capture.frames as wdmcf
import winsdk.windows.media.mediaproperties as wmmp

async def getCameras():
    frameSourceGroups = await wdmcf.MediaFrameSourceGroup.find_all_async()
    return frameSourceGroups

frameSourceGroups = asyncio.run(getCameras())
 


for currentSourceGroup in frameSourceGroups:
    for sourceInfo in currentSourceGroup.source_infos:
        if sourceInfo.media_stream_type == 0:
            if sourceInfo.source_kind == wdmcf.MediaFrameSourceInfo.source_kind.COLOR:
                break

selectedGroup = currentSourceGroup
colorSourceInfo = sourceInfo
print(selectedGroup)

mediaCapture = wdmc.MediaCapture()
settings = wdmc.MediaCaptureInitializationSettings()
settings.source_group = selectedGroup
settings.sharing_mode = wdmc.MediaCaptureSharingMode.EXCLUSIVE_CONTROL
settings.memory_preference = wdmc.MediaCaptureMemoryPreference.CPU
settings.streaming_capture_mode = wdmc.StreamingCaptureMode.VIDEO

async def initMediaCapture():
    await mediaCapture.initialize_async(settings)

try:
    asyncio.run(initMediaCapture())
except:
    print("failed to initialize mediacapture")

colorFrameSource = mediaCapture.frame_sources[colorSourceInfo.id]
for format in colorFrameSource.supported_formats:
    if format.video_format.width >= 0 and format.subtype == wmmp.MediaEncodingSubtypes.argb32:
        break
preferredFormat = format

async def setFormat():
    await colorFrameSource.set_format_async(preferredFormat)

asyncio.run(setFormat())