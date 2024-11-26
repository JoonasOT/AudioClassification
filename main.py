# Require Structures:
from typing import Final

# Required functions:
import numpy as np

from src.functions.file_management import *
from src.functions.audio_manipulation import FreqType, getNormalizedAudio, sampleTo, \
                                            limitSamplesTo, getSpectrum, getSpectrogram,\
                                            getMFCC
from src.functions.plotting import keepPlotsOpen


DATA_DIR: Final[str] = "./data"
TEST_DIR: Final[str] = "/test"
TRAIN_DIR: Final[str] = "/train"

SAMPLERATE: Final[int] = 22100
N_SAMPLES: Final[int] = int(2.0 * SAMPLERATE)

WIN_SIZE: Final[float] = 0.032
HOP_SIZE: Final[float] = WIN_SIZE / 2
N_MFCC: Final[int] = 40

MFCCs = {}


def main():
    for file in onlyWavFiles(getFilesInDir(DATA_DIR + TRAIN_DIR)):
        print(file)
        # Create a normalized AudioSignal
        audio = getNormalizedAudio(file, plot=False)

        # Form spectrums
        # spectrum = getSpectrum(audio, FreqType.DECIBEL, plot=False)

        # Form spectrograms
        # spectrogram = getSpectrogram(audio, FreqType.DECIBEL, WIN_SIZE, HOP_SIZE, plot=False)

        mfcc = getMFCC(audio, N_MFCC, WIN_SIZE, HOP_SIZE, plot=False)

        model = file.split("/")[-2]
        if model in MFCCs:
            MFCCs[model].append(np.mean(mfcc.unwrap().T, axis=0))
        else:
            MFCCs[model] = [np.mean(mfcc.unwrap().T, axis=0)]

    for file in onlyWavFiles(getFilesInDir(DATA_DIR + TEST_DIR)):
        print(file)
        # Create a normalized AudioSignal
        audio = getNormalizedAudio(file, plot=False)

        # Form spectrums
        # spectrum = getSpectrum(audio, FreqType.DECIBEL, plot=False)

        # Form spectrograms
        # spectrogram = getSpectrogram(audio, FreqType.DECIBEL, WIN_SIZE, HOP_SIZE, plot=False)

        mfcc = getMFCC(audio, N_MFCC, WIN_SIZE, HOP_SIZE, plot=False)

        for m, mfccs in MFCCs.items():
            dists = []
            for mfcc_ in mfccs:
                dists.append(np.linalg.norm(np.mean(mfcc.unwrap().T, axis=0) - mfcc_))
            dists = np.sort(dists)
            print(f"For {file} the matches for {m} where:\n{dists}")

    keepPlotsOpen()


if __name__ == '__main__':
    main()
