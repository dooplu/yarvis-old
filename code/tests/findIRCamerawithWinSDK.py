import asyncio
import winsdk.windows.media.capture as wdmc
import winsdk.windows.media.capture.frames as wdmcf
import winsdk.windows.media.mediaproperties as wmmp
import cv2 as cv
from PIL import Image

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
    if format.video_format.width >= 720 and format.subtype == 'argb32':
        break
preferredFormat = format
print(preferredFormat)

async def setFormat():
    await colorFrameSource.set_format_async(preferredFormat)

asyncio.run(setFormat())


async def getFrames():
    mediaFrameReader = await mediaCapture.create_frame_reader_async(colorFrameSource, 'argb32')
    mediaFrameReader.try_acquire_latest_frame()
    await mediaFrameReader.start_async()
    return mediaFrameReader
    

mediaFrameReader = asyncio.run(getFrames())

#img = mediaFrameReader.

#open("C:/Users/Adam/Desktop/img.txt", "wb").write(img)

#cv.imshow('Camera', img)