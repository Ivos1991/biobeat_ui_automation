"""Session lifecycle logging plugin."""

from core.framework.hooks import SessionContext, TestContext
from core.framework.plugins import plugin
from core.framework.runtime import FrameworkRuntime


@plugin("session_logger")
class SessionLoggerPlugin:
    """Emit structured logs for framework session and test lifecycle hooks."""

    name = "session_logger"
    description = "Logs session and test lifecycle transitions."

    def register(self, runtime: FrameworkRuntime) -> None:
        """Register the logging callbacks that track session and test lifecycle transitions."""
        def before_session(context: SessionContext) -> None:
            """Log the start of a framework session together with its execution environment."""
            runtime.logger.info(
                "Session %s started in %s", context.session_id, runtime.settings.runtime.environment.value
            )

        def before_test(context: TestContext) -> None:
            """Log the start of each collected test just before pytest setup runs."""
            runtime.logger.info("Starting test %s", context.nodeid)

        def after_test(context: TestContext) -> None:
            """Log the end of each test together with the final pytest outcome."""
            runtime.logger.info(
                "Finished test %s with outcome=%s", context.nodeid, context.outcome
            )

        runtime.hooks.register("before_session", before_session, owner=self.name, order=10)
        runtime.hooks.register("before_test", before_test, owner=self.name, order=20)
        runtime.hooks.register("after_test", after_test, owner=self.name, order=20)
