import argparse
import logging

# Imports needed for Clams and MMIF.
# Non-NLP Clams applications will require AnnotationTypes

from clams import ClamsApp, Restifier
from mmif import Mmif, View, Annotation, Document, AnnotationTypes, DocumentTypes

# For an NLP tool we need to import the LAPPS vocabulary items
from lapps.discriminators import Uri

from faster_whisper import WhisperModel
import tempfile
import ffmpeg

class FasterWhisper(ClamsApp):

    def __init__(self):
        super().__init__()

    def _appmetadata(self):
        pass

    def _annotate(self, mmif: Mmif, **parameters) -> Mmif:
        if not isinstance(mmif, Mmif):
            mmif: Mmif = Mmif(mmif)

        # get the file path
        docs = mmif.get_documents_by_type(DocumentTypes.AudioDocument)
        if docs:
            doc = docs[0]
            target_path = doc.location_path(nonexist_ok=False)
        else:
            docs = mmif.get_documents_by_type(DocumentTypes.VideoDocument)
            doc = docs[0]
            video_path = doc.location_path(nonexist_ok=False)
            # transform the video file to audio file
            audio_tmpdir = tempfile.TemporaryDirectory()
            target_path = f'{audio_tmpdir.name}/{doc.id}_16kHz.wav'
            ffmpeg.input(video_path).output(target_path, ac=1, ar=16000).run()
        
        new_view = mmif.new_view()
        self.sign_view(new_view, parameters)
        new_view.new_contain(DocumentTypes.TextDocument, document=doc.long_id)
        new_view.new_contain(AnnotationTypes.TimeFrame, timeUnit="milliseconds", document=doc.long_id)
        new_view.new_contain(AnnotationTypes.Alignment)
        new_view.new_contain(Uri.SENTENCE, document=doc.long_id)
        
        model_id = parameters['modelType']
        self.logger.debug(f'faster whisper model: {model_id})')

        device = parameters['device']
        if device == 'cpu':
            model = WhisperModel(model_id, device="cpu", compute_type="int8")
        elif device == 'gpu':
            model = WhisperModel(model_id, device="cuda", compute_type="float16")
        
        beam = parameters['beam_size']

        if 'distil' in model_id:
            segments, info = model.transcribe(target_path, beam_size=beam, language="en", condition_on_previous_text=False, word_timestamps=True)
        else:
            segments, info = model.transcribe(target_path, beam_size=beam, word_timestamps=True)
        
        text = ""
        char_offset = 0
        for segment in segments:
            s_text = segment.text[1:]
            if not text:
                text = s_text
            else:
                text = text + ' ' + s_text
            token_ids = []
            for word in segment.words:
                token = word.word[1:]
                tok_start = text.index(token, char_offset)
                tok_end = tok_start + len(token)
                char_offset = tok_end
                token = new_view.new_annotation(Uri.TOKEN, word=token, start=tok_start, end=tok_end)
                token_ids.append(token.id)   
                token_tf = new_view.new_annotation(AnnotationTypes.TimeFrame, frameType="speech", start=int(word.start * 1000), end=int(word.end * 1000))
                new_view.new_annotation(AnnotationTypes.Alignment, source=token_tf.long_id, target=token.long_id)
            tf = new_view.new_annotation(AnnotationTypes.TimeFrame, frameType="speech", start=int(segment.start * 1000), end=int(segment.end * 1000))
            sentence = new_view.new_annotation(Uri.SENTENCE, targets=token_ids, text=s_text)
            new_view.new_annotation(AnnotationTypes.Alignment, source=tf.long_id, target=sentence.long_id)
        textdoc = new_view.new_textdocument(text=text, lang='en')
        new_view.new_annotation(AnnotationTypes.Alignment, source=doc.long_id, target=textdoc.long_id)
    
        return mmif

        

def get_app():
    return FasterWhisper()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", action="store", default="5000", help="set port to listen")
    parser.add_argument("--production", action="store_true", help="run gunicorn server")
    # add more arguments as needed
    # parser.add_argument(more_arg...)

    parsed_args = parser.parse_args()

    # create the app instance
    # if get_app() call requires any "configurations", they should be set now as global variables
    # and referenced in the get_app() function. NOTE THAT you should not change the signature of get_app()
    app = get_app()

    http_app = Restifier(app, port=int(parsed_args.port))
    # for running the application in production mode
    if parsed_args.production:
        http_app.serve_production()
    # development mode
    else:
        app.logger.setLevel(logging.DEBUG)
        http_app.run()
