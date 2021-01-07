print('Loading TensorFlow and stuff...')
import numpy as np
import scipy.signal
import soundfile as sf
import tensorflow as tf

print('Loading YAMNet and hyperparameters...')
import params as yamnet_params
import yamnet as yamnet_model
params = yamnet_params.Params()
yamnet = yamnet_model.yamnet_frames_model(params)
yamnet.load_weights('yamnet.h5')
yamnet_classes = yamnet_model.class_names('yamnet_class_map_zh-tw.csv')

import os, pyaudio, time
#os.system('jack_control start')
p = pyaudio.PyAudio()
os.system('clear')
print('Sound Event Detection by making inference on every 1.024 second audio stream from the microphone!\n')

CHUNK = 1024 # frames_per_buffer # samples per chunk
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1.024#0.96                                 # 16 CHUNKs
INFERENCE_WINDOW = 1 * int(RATE / CHUNK * RECORD_SECONDS)   # 16 CHUNKs

stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

CHUNKs = []
while True:
    try:
        stream.start_stream()
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            CHUNKs.append(data)
            # print(len(CHUNKs))
        stream.stop_stream()

        if len(CHUNKs) > INFERENCE_WINDOW:
            CHUNKs = CHUNKs[int(RATE / CHUNK * RECORD_SECONDS):]
            # print('new len: ',len(CHUNKs))
        wav_data = np.frombuffer(b''.join(CHUNKs), dtype=np.int16)
        waveform = wav_data / tf.int16.max#32768.0
        waveform = waveform.astype('float32')
        scores, embeddings, spectrogram = yamnet(waveform)
        # print(scores.shape)
        # print(embeddings.shape)
        # print(spectrogram.shape)
        prediction = np.mean(scores[:-1], axis=0) # last score comes from insufficient samples
        # print(prediction.shape)
        top3 = np.argsort(prediction)[::-1][:3]
        print(time.ctime().split()[3], '\t',
            ''.join(f"{prediction[i]:.1f}👈{yamnet_classes[i][:11].ljust(11, '　')}" for i in top3))
    except:
        stream.stop_stream()
        stream.close()
        p.terminate()