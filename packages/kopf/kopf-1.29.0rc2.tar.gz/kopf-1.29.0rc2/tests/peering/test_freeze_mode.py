import asyncio
import dataclasses
from unittest.mock import Mock

import freezegun
import pytest

from kopf.engines.peering import process_peering_event
from kopf.structs import bodies, primitives


@dataclasses.dataclass(frozen=True, eq=False)
class K8sMocks:
    patch_obj: Mock


@pytest.fixture(autouse=True)
def k8s_mocked(mocker, resp_mocker):
    # We mock on the level of our own K8s API wrappers, not the K8s client.
    return K8sMocks(
        patch_obj=mocker.patch('kopf.clients.patching.patch_obj', return_value={}),
    )


@pytest.fixture
async def replenished(mocker):
    # Make sure that freeze-sleeps are not actually executed, i.e. exit instantly.
    replenished = asyncio.Event()
    replenished.set()
    mocker.patch.object(replenished, 'wait')  # to avoid RuntimeWarnings for unwaited coroutines
    return replenished


async def test_other_peering_objects_are_ignored(
        mocker, k8s_mocked, settings, replenished,
        peering_resource, peering_namespace):

    status = mocker.Mock()
    status.items.side_effect = Exception("This should not be called.")
    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'their-name'},
            'status': status,
        })

    wait_for = mocker.patch('asyncio.wait_for')

    settings.peering.name = 'our-name'
    await process_peering_event(
        raw_event=event,
        freeze_toggle=primitives.Toggle(),
        replenished=replenished,
        autoclean=False,
        identity='id',
        settings=settings,
        namespace=peering_namespace,
        resource=peering_resource,
    )
    assert not status.items.called
    assert not k8s_mocked.patch_obj.called
    assert wait_for.call_count == 0


@freezegun.freeze_time('2020-12-31T23:59:59.123456')
async def test_toggled_on_for_higher_priority_peer_when_initially_off(
        mocker, k8s_mocked, replenished, caplog, assert_logs, settings,
        peering_resource, peering_namespace):

    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'name', 'namespace': peering_namespace},  # for matching
            'status': {
                'higher-prio': {
                    'priority': 101,
                    'lifetime': 10,
                    'lastseen': '2020-12-31T23:59:59'
                },
            },
        })
    settings.peering.name = 'name'
    settings.peering.priority = 100

    freeze_toggle = primitives.Toggle(False)
    wait_for = mocker.patch('asyncio.wait_for')

    caplog.set_level(0)
    assert freeze_toggle.is_off()
    await process_peering_event(
        raw_event=event,
        freeze_toggle=freeze_toggle,
        replenished=replenished,
        autoclean=False,
        namespace=peering_namespace,
        resource=peering_resource,
        identity='id',
        settings=settings,
    )
    assert freeze_toggle.is_on()
    assert wait_for.call_count == 1
    assert 9 < wait_for.call_args[1]['timeout'] < 10
    assert not k8s_mocked.patch_obj.called
    assert_logs(["Freezing operations in favour of"], prohibited=[
        "Possibly conflicting operators",
        "Freezing all operators, including self",
        "Resuming operations after the freeze",
    ])


@freezegun.freeze_time('2020-12-31T23:59:59.123456')
async def test_ignored_for_higher_priority_peer_when_already_on(
        mocker, k8s_mocked, replenished, caplog, assert_logs, settings,
        peering_resource, peering_namespace):

    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'name', 'namespace': peering_namespace},  # for matching
            'status': {
                'higher-prio': {
                    'priority': 101,
                    'lifetime': 10,
                    'lastseen': '2020-12-31T23:59:59'
                },
            },
        })
    settings.peering.name = 'name'
    settings.peering.priority = 100

    freeze_toggle = primitives.Toggle(True)
    wait_for = mocker.patch('asyncio.wait_for')

    caplog.set_level(0)
    assert freeze_toggle.is_on()
    await process_peering_event(
        raw_event=event,
        freeze_toggle=freeze_toggle,
        replenished=replenished,
        autoclean=False,
        namespace=peering_namespace,
        resource=peering_resource,
        identity='id',
        settings=settings,
    )
    assert freeze_toggle.is_on()
    assert wait_for.call_count == 1
    assert 9 < wait_for.call_args[1]['timeout'] < 10
    assert not k8s_mocked.patch_obj.called
    assert_logs([], prohibited=[
        "Possibly conflicting operators",
        "Freezing all operators, including self",
        "Freezing operations in favour of",
        "Resuming operations after the freeze",
    ])


@freezegun.freeze_time('2020-12-31T23:59:59.123456')
async def test_toggled_off_for_lower_priority_peer_when_initially_on(
        mocker, k8s_mocked, replenished, caplog, assert_logs, settings,
        peering_resource, peering_namespace):

    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'name', 'namespace': peering_namespace},  # for matching
            'status': {
                'higher-prio': {
                    'priority': 99,
                    'lifetime': 10,
                    'lastseen': '2020-12-31T23:59:59'
                },
            },
        })
    settings.peering.name = 'name'
    settings.peering.priority = 100

    freeze_toggle = primitives.Toggle(True)
    wait_for = mocker.patch('asyncio.wait_for')

    caplog.set_level(0)
    assert freeze_toggle.is_on()
    await process_peering_event(
        raw_event=event,
        freeze_toggle=freeze_toggle,
        replenished=replenished,
        autoclean=False,
        namespace=peering_namespace,
        resource=peering_resource,
        identity='id',
        settings=settings,
    )
    assert freeze_toggle.is_off()
    assert wait_for.call_count == 0
    assert not k8s_mocked.patch_obj.called
    assert_logs(["Resuming operations after the freeze"], prohibited=[
        "Possibly conflicting operators",
        "Freezing all operators, including self",
        "Freezing operations in favour of",
    ])


@freezegun.freeze_time('2020-12-31T23:59:59.123456')
async def test_ignored_for_lower_priority_peer_when_already_off(
        mocker, k8s_mocked, replenished, caplog, assert_logs, settings,
        peering_resource, peering_namespace):

    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'name', 'namespace': peering_namespace},  # for matching
            'status': {
                'higher-prio': {
                    'priority': 99,
                    'lifetime': 10,
                    'lastseen': '2020-12-31T23:59:59'
                },
            },
        })
    settings.peering.name = 'name'
    settings.peering.priority = 100

    freeze_toggle = primitives.Toggle(False)
    wait_for = mocker.patch('asyncio.wait_for')

    caplog.set_level(0)
    assert freeze_toggle.is_off()
    await process_peering_event(
        raw_event=event,
        freeze_toggle=freeze_toggle,
        replenished=replenished,
        autoclean=False,
        namespace=peering_namespace,
        resource=peering_resource,
        identity='id',
        settings=settings,
    )
    assert freeze_toggle.is_off()
    assert wait_for.call_count == 0
    assert not k8s_mocked.patch_obj.called
    assert_logs([], prohibited=[
        "Possibly conflicting operators",
        "Freezing all operators, including self",
        "Freezing operations in favour of",
        "Resuming operations after the freeze",
    ])


@freezegun.freeze_time('2020-12-31T23:59:59.123456')
async def test_toggled_on_for_same_priority_peer_when_initially_off(
        mocker, k8s_mocked, replenished, caplog, assert_logs, settings,
        peering_resource, peering_namespace):

    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'name', 'namespace': peering_namespace},  # for matching
            'status': {
                'higher-prio': {
                    'priority': 100,
                    'lifetime': 10,
                    'lastseen': '2020-12-31T23:59:59'
                },
            },
        })
    settings.peering.name = 'name'
    settings.peering.priority = 100

    freeze_toggle = primitives.Toggle(False)
    wait_for = mocker.patch('asyncio.wait_for')

    caplog.set_level(0)
    assert freeze_toggle.is_off()
    await process_peering_event(
        raw_event=event,
        freeze_toggle=freeze_toggle,
        replenished=replenished,
        autoclean=False,
        namespace=peering_namespace,
        resource=peering_resource,
        identity='id',
        settings=settings,
    )
    assert freeze_toggle.is_on()
    assert wait_for.call_count == 1
    assert 9 < wait_for.call_args[1]['timeout'] < 10
    assert not k8s_mocked.patch_obj.called
    assert_logs([
        "Possibly conflicting operators",
        "Freezing all operators, including self",
    ], prohibited=[
        "Freezing operations in favour of",
        "Resuming operations after the freeze",
    ])


@freezegun.freeze_time('2020-12-31T23:59:59.123456')
async def test_ignored_for_same_priority_peer_when_already_on(
        mocker, k8s_mocked, replenished, caplog, assert_logs, settings,
        peering_resource, peering_namespace):

    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'name', 'namespace': peering_namespace},  # for matching
            'status': {
                'higher-prio': {
                    'priority': 100,
                    'lifetime': 10,
                    'lastseen': '2020-12-31T23:59:59'
                },
            },
        })
    settings.peering.name = 'name'
    settings.peering.priority = 100

    freeze_toggle = primitives.Toggle(True)
    wait_for = mocker.patch('asyncio.wait_for')

    caplog.set_level(0)
    assert freeze_toggle.is_on()
    await process_peering_event(
        raw_event=event,
        freeze_toggle=freeze_toggle,
        replenished=replenished,
        autoclean=False,
        namespace=peering_namespace,
        resource=peering_resource,
        identity='id',
        settings=settings,
    )
    assert freeze_toggle.is_on()
    assert wait_for.call_count == 1
    assert 9 < wait_for.call_args[1]['timeout'] < 10
    assert not k8s_mocked.patch_obj.called
    assert_logs([
        "Possibly conflicting operators",
    ], prohibited=[
        "Freezing all operators, including self",
        "Freezing operations in favour of",
        "Resuming operations after the freeze",
    ])


@freezegun.freeze_time('2020-12-31T23:59:59.123456')
@pytest.mark.parametrize('priority', [100, 101])
async def test_resumes_immediately_on_expiration_of_blocking_peers(
        mocker, k8s_mocked, replenished, caplog, assert_logs, settings, priority,
        peering_resource, peering_namespace):

    event = bodies.RawEvent(
        type='ADDED',  # irrelevant
        object={
            'metadata': {'name': 'name', 'namespace': peering_namespace},  # for matching
            'status': {
                'higher-prio': {
                    'priority': priority,
                    'lifetime': 10,
                    'lastseen': '2020-12-31T23:59:59'
                },
            },
        })
    settings.peering.name = 'name'
    settings.peering.priority = 100

    freeze_toggle = primitives.Toggle(True)
    wait_for = mocker.patch('asyncio.wait_for', side_effect=asyncio.TimeoutError)

    caplog.set_level(0)
    assert freeze_toggle.is_on()
    await process_peering_event(
        raw_event=event,
        freeze_toggle=freeze_toggle,
        replenished=replenished,
        autoclean=False,
        namespace=peering_namespace,
        resource=peering_resource,
        identity='id',
        settings=settings,
    )
    assert freeze_toggle.is_on()
    assert wait_for.call_count == 1
    assert 9 < wait_for.call_args[1]['timeout'] < 10
    assert k8s_mocked.patch_obj.called
