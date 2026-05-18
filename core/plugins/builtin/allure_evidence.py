"""Allure-oriented evidence plugin for failures and API calls."""

import json

from core.framework.hooks import ApiCallContext, FailureContext
from core.framework.plugins import plugin
from core.reporting import attach_json, attach_text


@plugin("allure_evidence")
class AllureEvidencePlugin:
    """Attach failure metadata and API traces to Allure through hooks."""

    name = "allure_evidence"
    description = "Captures framework evidence for failures and API interactions."

    def register(self, runtime) -> None:
        def after_api_call(context: ApiCallContext) -> None:
            payload = {
                "client": context.client_name,
                "method": context.method,
                "url": context.url,
                "expected_statuses": list(context.expected_statuses),
                "status_code": context.status_code,
                "duration_ms": context.duration_ms,
            }
            attach_json("api-call", payload)
            if context.error is not None:
                attach_text("api-call-error", repr(context.error))
            if context.response_payload is not None and isinstance(context.response_payload, (dict, list)):
                attach_json("api-response", context.response_payload)
            elif context.response_payload is not None:
                attach_text("api-response", json.dumps(context.response_payload, default=str))

        def on_failure(context: FailureContext) -> None:
            attach_text("failed-test", context.test.nodeid)
            if context.error is not None:
                attach_text("failure-exception", repr(context.error))
            if context.report is not None:
                attach_text("failure-longrepr", str(getattr(context.report, "longrepr", "")))

        runtime.hooks.register("after_api_call", after_api_call, owner=self.name, order=50)
        runtime.hooks.register("on_failure", on_failure, owner=self.name, order=50)
