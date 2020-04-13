import os
from google.cloud import language
from google.cloud.language import types
from google.cloud.language import enums
from google.oauth2 import service_account

GOOGLE_CREDENTIALS_PATH = os.environ.get('GOOGLE_CREDENTIALS_PATH')
credentials: service_account.Credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_PATH, scopes=[
        "https://www.googleapis.com/auth/cloud-platform"])
client = language.LanguageServiceClient(credentials=credentials)


def analyze_sentiment(text: str):
    return client.analyze_sentiment(document=types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT))
