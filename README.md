# Faster-Whisper Wrapper

## Description
Wrapper for Faster-Whisper https://github.com/SYSTRAN/faster-whisper

## Input
The wrapper takes miff file which refers to either an AudioDocument or a VideoDocument. You can choose the
specific model you want to use by add parameter. Faster-whisper support all the models from both distil-whisper and open-ai origin whisper. For distil-whisper, you can choose :"distil-large-v2", "distil-large-v3", "distil-small.en", "distil-medium.en". For original whisper, you can choose:"large-v3", "large-v2", "large-v1", "medium.en", "medium", "base.en", "base", "small.en", "small", "tiny.en", "tiny". The default model is "distil-small.en ".
There are two other parameters you can use. First, you can choose either "CPU" or "GPU" on device parameter. The default device is cpu. Besides, there is a beam_size parameter, enter the number of beam size you want. The default number is 5.

## Output
The output miff file will contain four objects: **Uri.TOKEN**, which is the smallest text unit recognized by the faster-whisper; **Uri.SENTENCE**, the segmental level of recoginzed texts; **AnnotationTypes.TimeFrame**, which represents the timeframe that each sentences and each words take place; **DocumentTypes.TextDocument**, which contains all the text recognized by faster-whisper in the whole audio/video; **AnnotationTypes.BoundingBox**, which show the alignments between `Timeframe` <-> `SENTENCE`, `Timeframe` <-> `TOKEN`, and `audio/video` <-> `TextDocument`.

## User instruction
General user instructions for CLAMS apps are available at CLAMS Apps documentation: https://apps.clams.ai/clamsapp/

### System requirements
- Requires faster_whisper
- Requires **ffmpeg-python** for the VideoDocument
