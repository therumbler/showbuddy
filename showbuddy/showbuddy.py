import boto3


class ShowBuddy:
    def __init__(self):
        self._s3 = boto3.client("s3")
        self._s3_bucket = "showbuddy"

    def _process_business_card(self, business_card_filepath):
        pass

    def _process_business_cards(self, business_card_filepaths):
        return list(map(self._process_business_card, business_card_filepaths))

    def _process_audio(self, audio_filepath):
        pass

    def process(self, audio_filepath, business_card_filepaths):
        # get audio data
        # upload audio data to s3
        # get s3 url
        # call fireflies api with s3 url
        # get transcript
        # tag timestamp
        #
        pass


def test():
    """test things"""
    showbuddy = ShowBuddy()
    assert showbuddy is not None
    print("All tests pass")
