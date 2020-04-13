import os
import typing
from google.cloud import bigquery
from google.oauth2 import service_account

GOOGLE_CREDENTIALS_PATH = os.environ.get('GOOGLE_CREDENTIALS_PATH')
BQML_DATASET = 'data'
BQML_TEST_TABLE = 'better_model_test'
BQML_FULL_TEST_TABLE = '%s.%s' % (BQML_DATASET, BQML_TEST_TABLE)
credentials: service_account.Credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_PATH, scopes=[
        "https://www.googleapis.com/auth/cloud-platform"])
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


def clear_test_data():
    client.query("DELETE FROM %s WHERE 1=1" % BQML_FULL_TEST_TABLE)


def setup_test_data(rows: typing.List[dict]) -> typing.Optional[typing.List[dict]]:
    table: bigquery.Table = client.get_table(BQML_FULL_TEST_TABLE)
    errors = client.insert_rows(table, rows)

    return errors if errors else None


def predict_data() -> typing.Generator[bigquery.Row, None, None]:
    """
    SELECT * FROM ML.PREDICT(MODEL data.better_model, (
      SELECT
        name,
        followers_count,
        friends_count,
        verified,
        statuses_count,
        (friends_count / GREATEST(followers_count, 1)) AS friends_to_followers_ratio,
        (statuses_count / DATETIME_DIFF(CURRENT_DATETIME(), created_at, HOUR)) AS tweets_per_hour,
        CHAR_LENGTH(name) AS name_length,
        default_profile_image
      FROM data.better_model_test
    ))
    :return:
    """

    job: bigquery.job.QueryJob = client.query(
        """
        SELECT * FROM ML.PREDICT(MODEL data.better_model, (
          SELECT
            name,
            followers_count,
            friends_count,
            verified,
            statuses_count,
            (friends_count / GREATEST(followers_count, 1)) AS friends_to_followers_ratio,
            (statuses_count / DATETIME_DIFF(CURRENT_DATETIME(), created_at, DAY)) AS tweets_per_day,
            default_profile_image
          FROM data.better_model_test
        ))
        """
    )

    for x in job:
        yield x
