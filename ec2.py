import json


def get_ec2_instances() -> dict:
    with open("ec2.json") as f:
        response = json.load(f)

    all_instances = [
        instance
        for reservation in response.get("Reservations", [])
        for instance in reservation.get("Instances", [])
    ]
    f.close()
    return all_instances


def is_instance_running(instance: dict) -> bool:
    return instance.get("State", {}).get("Name") == "running"


def get_instances_running(instances: dict) -> dict:
    running_instances = list(filter(is_instance_running, instances))
    instance_status = {"total": len(instances), "running": len(running_instances)}
    return instance_status

if __name__ == "__main__":
    ec2 = get_ec2_instances()
    get_instances_running(ec2)
