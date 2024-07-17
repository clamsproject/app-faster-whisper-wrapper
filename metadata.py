"""
The purpose of this file is to define the metadata of the app with minimal imports.

DO NOT CHANGE the name of the file
"""

from mmif import DocumentTypes, AnnotationTypes

from clams.app import ClamsApp
from clams.appmetadata import AppMetadata
from lapps.discriminators import Uri


# DO NOT CHANGE the function name
def appmetadata() -> AppMetadata:
    """
    Function to set app-metadata values and return it as an ``AppMetadata`` obj.
    Read these documentations before changing the code below
    - https://sdk.clams.ai/appmetadata.html metadata specification.
    - https://sdk.clams.ai/autodoc/clams.appmetadata.html python API
    
    :return: AppMetadata object holding all necessary information.
    """
    
    # first set up some basic information
    metadata = AppMetadata(
        name="Fast Whisper Wrapper",
        description="The wrapper of Fast Whisper. 15 models avaliable, 4 for distil-whisper, 11 for whisper. 1. faster-distil-whisper-large-v2 2. faster-distil-whisper-large-v3 3. faster-distil-whisper-small.en 4. faster-distil-whisper-medium.en 5. faster-whisper-large-v2 6. faster-whisper-large-v1 7. faster-whisper-medium.en 8. faster-whisper-medium 9. faster-whisper-base.en 10. faster-whisper-base 11. faster-whisper-small.en 12. faster-whisper-small 13. faster-whisper-tiny.en 14. faster-whisper-tiny 15. faster-whisper-large-v3",
        app_license="Apache 2.0",  # short name for a software license like MIT, Apache2, GPL, etc.
        identifier="fast-whisper",  # should be a single string without whitespaces. If you don't intent to publish this app to the CLAMS app-directory, please use a full IRI format.
        url="https://fakegithub.com/some/repository",  # a website where the source code and full documentation of the app is hosted
        analyzer_version='', # use this IF THIS APP IS A WRAPPER of an existing computational analysis algorithm
        analyzer_license="MIT",  # short name for a software license
    )
    # and then add I/O specifications: an app must have at least one input and one output
    metadata.add_input_oneof(DocumentTypes.AudioDocument, DocumentTypes.VideoDocument)
    out_td = metadata.add_output(DocumentTypes.TextDocument, **{'@lang': 'en'})
    out_td.add_description('Fully serialized text content of the recognized text in the input audio/video.')
    timeunit = "milliseconds"
    metadata.add_output(AnnotationTypes.TimeFrame, timeUnit=timeunit)
    out_ali = metadata.add_output(AnnotationTypes.Alignment)
    out_ali.add_description('Alignments between 1) `TimeFrame` <-> `SENTENCE`, 3) `TimeFrame` <-> `Token`, 2) `audio/video document` <-> `TextDocument`')
    out_sent = metadata.add_output(Uri.SENTENCE)
    out_sent.add_description('The smallest recognized unit of distil-whisper. Normally a complete sentence.')
    metadata.add_output(Uri.TOKEN)
    
    metadata.add_parameter(
        name='modelType', 
        description='The type of the model to use. Both distil-whsiper and whisper are avaliable 1. distil-whisper-large-v2 2. distil-whisper-large-v3 3. distil-whisper-small.en 4. distil-whisper-medium.en 5. whisper-large-v2 6. whisper-large-v1 7. whisper-medium.en 8. whisper-medium 9. whisper-base.en 10. whisper-base 11. whisper-small.en 12. whisper-small 13. whisper-tiny.en 14. whisper-tiny 15. whisper-large-v3',
        type='string',
        choices=["distil-large-v2 "
                    "distil-large-v3 "
                    "distil-small.en "
                    "distil-medium.en "
                    "large-v2 "
                    "large-v1 "
                    "medium.en "
                    "medium "
                    "base.en "
                    "base "
                    "small.en "
                    "small "
                    "iny.en "
                    "tiny "
                    "large-v3"],
        default='distil-small.en')
    
    metadata.add_parameter(
        name='device', 
        description='Run on GPU with FP16, or run on CPU with INT8, default is cpu',
        type='string',
        choices=['cpu', 'gpu'],
        default='cpu')

    metadata.add_parameter(
        name='beam_size', 
        description='Beam size controls the number of paths that are explored at each step when generating an output',
        type='integer',
        default=5)
    
    # CHANGE this line and make sure return the compiled `metadata` instance
    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    metadata = appmetadata()
    for param in ClamsApp.universal_parameters:
        metadata.add_parameter(**param)
    sys.stdout.write(metadata.jsonify(pretty=True))
