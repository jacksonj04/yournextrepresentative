from django.test import TestCase, override_settings
import json
from mock import patch, Mock

from utils.slack import SlackHelper

from parties.tests.factories import PartyFactory


class TestSlack(TestCase):
    @patch("slacker.requests")
    @override_settings(SLACK_TOKEN="FAKE")
    def test_post_to_slack(self, mock_requests):
        text = {"ok": "true"}
        mock_requests.post.return_value = Mock(
            status_code=200, text=json.dumps(text)
        )

        client = SlackHelper()
        client.post_message("#general", "testing")

        mock_requests.post.assert_called_with(
            "https://slack.com/api/chat.postMessage",
            timeout=10,
            proxies={},
            data={
                "channel": "#general",
                "text": "testing",
                "username": "CandidateBot",
                "as_user": None,
                "parse": None,
                "link_names": None,
                "attachments": None,
                "unfurl_links": None,
                "unfurl_media": None,
                "icon_url": None,
                "icon_emoji": ":robot_face:",
                "thread_ts": None,
                "reply_broadcast": None,
            },
            params={"token": "FAKE"},
        )

    @patch("slacker.requests")
    @override_settings(SLACK_TOKEN="FAKE")
    def test_post_party_as_attachment(self, mock_requests):
        text = {"ok": "true"}
        mock_requests.post.return_value = Mock(
            status_code=200, text=json.dumps(text)
        )
        party = PartyFactory(ec_id="PP33", __sequence=99)

        client = SlackHelper()
        client.post_message(
            "#candidates",
            message_text="A new party is born!",
            attachments=[p.as_slack_attachment for p in [party]],
        )
        called_args = mock_requests.post.call_args

        self.assertEqual(
            called_args[0], ("https://slack.com/api/chat.postMessage",)
        )
        kwargs = called_args[1]
        self.assertEqual(kwargs["data"]["channel"], "#candidates")
        self.assertEqual(kwargs["data"]["text"], "A new party is born!")
        self.assertEqual(kwargs["data"]["username"], "CandidateBot")
