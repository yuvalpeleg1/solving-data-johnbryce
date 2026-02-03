import boto3
from dotenv import load_dotenv

load_dotenv()


def get_ec2_instances(ec2) -> dict:
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


if __name__ == "__main__":
    ec2 = boto3.client("ec2")
    instances = get_ec2_instances(ec2)
    result = get_instances_running(instances)
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
