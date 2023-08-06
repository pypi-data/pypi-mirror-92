"""
Example CRUD routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""
from typing import Optional

from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    is_,
)
from hamcrest.core.base_matcher import BaseMatcher

from microcosm_sagemaker.testing.route import RouteTestCase


class InvocationsRouteTestCase(RouteTestCase):
    """
    Helper base class for writing tests of the invocations route.

    """

    request_json: dict
    response_items_matcher: Optional[BaseMatcher] = None
    expected_status_code: int = 200

    def test_search(self) -> None:
        """
        Invokes the invocations endpoint with `request_json`, and checks the
        `items` entry of the response against `response_items_matcher`.

        """
        uri = "/api/v1/invocations"

        response = self.client.post(
            uri,
            json=self.request_json,
        )

        assert_that(response.status_code, is_(equal_to(self.expected_status_code)))

        if self.response_items_matcher:
            assert_that(
                response.json,
                has_entries(
                    items=self.response_items_matcher,
                ),
            )
