from ctypes import *
import numpy as np

dll = cdll.LoadLibrary("/Users/tsurugiugushiro/Documents/HomeWork/2022.9/M-Intelligent_Prototype/modules/MLaughing/libLPC.dylib")
LPC = dll.LPC

def get_audio_frames(audio_data, rate=16000, frames_per_second = 30, chunks_length = 260):
    signal = audio_data
    audio_frameNum = int(len(signal) / rate * frames_per_second)
    a = np.zeros(chunks_length * rate // 1000, dtype=np.int16)
    signal = np.hstack((a, signal, a))
    signal = signal / (2. ** 15)
    frames_step = 1000.0 / frames_per_second
    rate_kHz = int(rate / 1000) 
    audio_frames = [
        signal[int(i * frames_step * rate_kHz): int((i * frames_step + chunks_length * 2) * rate_kHz)]
          for i in range(audio_frameNum)
          ]
    return audio_frames

def c_lpc(audio_frames_data, rate=16000, frames_per_second = 30, chunks_length = 260, overlap_frames_apart=0.008, numberOfFrames=64):
    inputData_array = np.zeros(shape=(1, 32, 64))
    overlap = int(rate * overlap_frames_apart)
    frameSize = int(rate * overlap_frames_apart * 2)
    frames = np.ndarray((numberOfFrames, frameSize))
    for i in range(len(audio_frames_data)):
        audio_frame = audio_frames_data[i] 
        for k in range(0, numberOfFrames):
            frames[k, :] = audio_frame[k * overlap:k * overlap + frameSize]
        k = numberOfFrames - 1
        for i in range(0, frameSize):
            if ((k * overlap + i) < len(audio_frame)):
                frames[k][i] = audio_frame[k * overlap + i]
            else:
                frames[k][i] = 0
        frames *= np.hanning(frameSize)
        frames_lpc_features = []
        a = (c_double * frameSize)()
        b = (c_double * 32)()
        for k in range(0, numberOfFrames):
            a = (c_double * frameSize)(*frames[k])
            LPC(pointer(a), frameSize, 32, pointer(b))
            frames_lpc_features.append(list(b))

        image_temp1 = np.array(frames_lpc_features)
        image_temp2 = image_temp1.transpose()
        image_temp3 = np.expand_dims(image_temp2, axis=0)
        inputData_array = np.concatenate((inputData_array, image_temp3),
                                         axis=0)
    inputData_array = inputData_array[1:]
    inputData_array = np.expand_dims(inputData_array, axis=3)
    return inputData_array
