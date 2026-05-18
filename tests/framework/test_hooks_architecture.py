import logging

from core.framework.hooks import HookManager, TestContext as HookTestContext
from core.framework.types import TestId


def test_hook_manager_ordered_execution_expects_handler_sequence():
    hook_manager = HookManager(logging.getLogger("test"))
    execution_order: list[str] = []
    context = HookTestContext(test_id=TestId("test-id"), nodeid="tests::ordered", name="ordered")

    hook_manager.register("before_test", lambda _context: execution_order.append("second"), order=20, owner="two")
    hook_manager.register("before_test", lambda _context: execution_order.append("first"), order=10, owner="one")

    hook_manager.emit("before_test", context)

    assert execution_order == ["first", "second"]


def test_hook_manager_fault_isolation_expects_noncritical_failure_not_to_stop_execution():
    hook_manager = HookManager(logging.getLogger("test"))
    execution_order: list[str] = []
    context = HookTestContext(test_id=TestId("test-id"), nodeid="tests::fault", name="fault")

    def fail(_context):
        execution_order.append("failed")
        raise RuntimeError("boom")

    hook_manager.register("after_test", fail, order=10, owner="failing")
    hook_manager.register("after_test", lambda _context: execution_order.append("continued"), order=20, owner="next")

    failures = hook_manager.emit("after_test", context)

    assert len(failures) == 1
    assert execution_order == ["failed", "continued"]
