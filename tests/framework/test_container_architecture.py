from core.framework.container import ContainerError, ServiceContainer


def test_service_container_singleton_resolution_expects_shared_instance():
    container = ServiceContainer()
    container.register_singleton("counter", instance={"value": 1})

    first = container.resolve("counter")
    second = container.resolve("counter")

    assert first is second


def test_service_container_factory_resolution_expects_new_instance_per_request():
    container = ServiceContainer()
    container.register_factory("factory", lambda _container: [])

    first = container.resolve("factory")
    second = container.resolve("factory")

    assert first is not second


def test_service_container_missing_dependency_expects_resolution_error():
    container = ServiceContainer()

    try:
        container.resolve("missing")
    except ContainerError as error:
        assert "missing" in str(error)
    else:
        raise AssertionError("Resolving an unknown dependency should fail")
