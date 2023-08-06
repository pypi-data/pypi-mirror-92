import json
import requests


class PostMattermost:

    def __init__(self, _attachments):
        self.attachments = _attachments

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Attachment:

    def __init__(self, _fallback, _color, _text, _title, _title_link, _fields):
        self.fallback = _fallback
        self.color = _color
        self.text = _text
        self.title = _title
        self.title_link = _title_link
        self.fields = _fields


class Field:

    def __init__(self, _short, _title, _value):
        self.short = _short
        self.title = _title
        self.value = _value


def send_file_to_mattermost(url_webhook, ci_project_url, ci_job_id, title):
    """

    :param url_webhook:
    :param ci_project_url:
    :param ci_job_id:
    :param title:
    :return:
    """

    attachment = Attachment("Gitlab Artifact download",
                            "#FF8000",
                            "Gitlab Artifact download link CI-JOB : " + ci_job_id,
                            title,
                            ci_project_url + "/-/jobs/" + str(ci_job_id) + "/artifacts/download?file_type=archive",
                            None,
                            [])

    push_post_mattermost(attachment, url_webhook)


def send_rss_to_mattermost(url_webhook, title, title_link, publish_date, author, users_mentioned, content):
    """

    :param url_webhook:
    :param title:
    :param title_link:
    :param publish_date:
    :param author:
    :param users_mentioned:
    :param content:
    :return:
    """

    field_users_mentioned = Field(False, "Users mentioned", users_mentioned)
    field_author = Field(False, "Author", author)
    field_publish_date = Field(False, "Publish date", publish_date)

    fields = [field_users_mentioned, field_author, field_publish_date]
    attachment = Attachment("Gitlab RSS Feed",
                            "#FF8000",
                            content,
                            title,
                            title_link,
                            fields)

    push_post_mattermost(attachment, url_webhook)


def push_post_mattermost(attachment, url_webhook):
    """

    :param attachment:
    :param url_webhook:
    :return:
    """

    post_mattermost = PostMattermost([attachment])

    payload = post_mattermost.to_json()
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        requests.request("POST", url_webhook, headers=headers, data=payload)
    except requests.exceptions.HTTPError as exception:
        print(exception)
        exit(0)
    except requests.exceptions.ConnectionError as exception:
        print(exception)
        exit(0)
