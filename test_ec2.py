import json
from ec2 import is_instance_running, get_instances_running

# Sample fake EC2 data for testing
fake_instances = [
    {"InstanceId": "i-1", "State": {"Name": "running"}},
    {"InstanceId": "i-2", "State": {"Name": "stopped"}},
    {"InstanceId": "i-3", "State": {"Name": "running"}},
    {"InstanceId": "i-4", "State": {"Name": "terminated"}},
]

with open("ec2.json") as f:
    response = json.load(f)
all_instances = [
    instance
    for reservation in response.get("Reservations", [])
    for instance in reservation.get("Instances", [])
]


def test_is_instance_running():
    assert is_instance_running(fake_instances[0]) is True
    assert is_instance_running(fake_instances[1]) is False
    assert is_instance_running(fake_instances[3]) is False
    for i in range(len(all_instances)):
        assert is_instance_running(all_instances[i])


def test_get_instances_running():
    result = get_instances_running(fake_instances)
    assert result["total"] == 4
    assert result["running"] == 2


def test_empty_instances():
    result = get_instances_running([])
    assert result["total"] == 0
    assert result["running"] == 0
