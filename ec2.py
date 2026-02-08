import json
import boto3
from dotenv import load_dotenv
from argparse import ArgumentParser

load_dotenv()


def get_ec2_instances(ec2) -> dict:
    if ec2 is None:
        with open("ec2.json", "r") as f:
            response = json.load(f)
    else:
        response = ec2.describe_instances()
    all_instances = [
        instance
        for reservation in response.get("Reservations", [])
        for instance in reservation.get("Instances", [])
    ]
    return all_instances


def stop_instances(ec2, ids: list[str]):
    response = ec2.stop_instances(InstanceIds=ids)
    print(response)


def start_instances(ec2, ids: list[str]):
    response = ec2.start_instances(InstanceIds=ids)
    print(response)


def is_instance_running(instance: dict) -> bool:
    return instance.get("State", {}).get("Name") == "running"


def get_instances_running(instances: dict) -> dict:
    running_instances = list(filter(is_instance_running, instances))
    instance_status = {"total": len(instances), "running": len(running_instances)}
    return instance_status


def flip_instance_state(instance: dict):
    if instance["State"]["Name"] == "running":
        print("Stopping instance")
    else:
        print("Starting instance")


def print_all(instances: dict):
    for index, instance in enumerate(instances):
        instance_type = instance["InstanceType"]
        instance_id = instance["InstanceId"]
        instance_state = instance["State"]["Name"].capitalize()
        entry = f"{index + 1}. {instance_type} ({instance_id}) - {instance_state}"
        print(entry)
    while True:
        user_choice = input(
            """Choose a machine to change state (running=>stopped / stopped=>running): """
        )
        try:
            user_choice = int(user_choice)
            if user_choice > len(instances) or user_choice <= 0:
                print("The number is out of range")
            else:
                break
        except ValueError:
            print("Enter only numbers")
    flip_instance_state(instances[user_choice - 1])


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--start", nargs="+", default=[])
    parser.add_argument("--stop", nargs="+", default=[])
    args = parser.parse_args()
    print(args)
    exit()

    # ec2 = boto3.client("ec2")
    ec2 = None
    instances = get_ec2_instances(ec2)
    result = print_all(instances)
    print(result)

    # --------Create and upload to S3--------
    # s3 = boto3.client("s3")
    # s3.create_bucket(Bucket="jb-yuvalp-devops-example")
    # s3.upload_file(Filename="1.txt", Key="folder1/uploads/files.txt", Bucket="jb-yuvalp-devops-example")
    # s3.put_object(Body=b"1.txt", Key="folder1/uploads/files.txt", Bucket="jb-yuvalp-devops-example")
    # s3.download_file(Filename="new.txt" ,Key="folder1/uploads/files.txt", Bucket="jb-yuvalp-devops-example")

    # --------Gives instances Ids by resource--------
    # ec2 = boto3.resource("ec2")
    # instances = ec2.instances.all()
    # for instance in instances:
    #     print(instance)
