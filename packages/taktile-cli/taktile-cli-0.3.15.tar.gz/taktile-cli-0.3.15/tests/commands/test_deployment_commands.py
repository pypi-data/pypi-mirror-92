import pytest
from pydantic import UUID4

from tktl.commands.deployments import GetDeployments, GetEndpoints
from tktl.core.exceptions.exceptions import APIClientException
from tktl.login import logout


def test_get_deployment_commands(logged_in_context):
    cmd = GetDeployments()
    result = cmd.execute(
        UUID4("33fb5b8f-e6a2-4dd2-86ef-d257d2c59b85"), None, None, None, None, None
    )
    print(result)
    assert len(result) == 1

    result = cmd.execute(None, None, None, None, None, None, return_all=True)
    assert len(result) >= 3

    cmd = GetEndpoints()
    result = cmd.execute(
        UUID4("28d4275b-072b-487c-a7e7-5898ce2bf1a4"),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )
    assert len(result) == 1

    cmd = GetDeployments()
    with pytest.raises(APIClientException):
        logout()
        cmd.execute(
            UUID4("7c0f6f48-0220-450a-b4d2-bfc731f94cc3"), None, None, None, None, None
        )
