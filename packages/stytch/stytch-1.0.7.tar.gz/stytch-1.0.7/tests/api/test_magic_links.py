import pytest
import stytch


class TestAuthenticate:
    def test_invalid_options_leads_to_error(self):
        stytch_client = stytch.Client(
            project_id="project_id",
            secret="secret",
            environment="live",
        )
        with pytest.raises(Exception) as error:
            stytch_client.MagicLinks.authenticate(
                token="token", options={"invalid_arg": "invalid"}
            )

    def test_invalid_project_id_status(self):
        stytch_client = stytch.Client(
            project_id="project_id",
            secret="secret",
            environment="live",
        )
        with pytest.raises(PermissionError) as error:
            stytch_client.MagicLinks.authenticate(token="token")
