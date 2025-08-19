import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
import os

DESTINATION_ROLE_ARN = os.environ['DESTINATION_ROLE_ARN']
DESTINATION_TABLE_NAME = os.environ['DESTINATION_TABLE_NAME']
DESTINATION_REGION = os.environ['DESTINATION_REGION']

deserializer = TypeDeserializer()

def deserialize_dynamodb_item(deserialized_item):
    return {k: deserializer.deserialize(v) for k, v in deserialized_item.items()}

def assume_cross_account_role():
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=DESTINATION_ROLE_ARN,
        RoleSessionName='DynamoDBReplication'
    )
    credentials = assumed_role['Credentials']
    dynamodb_dest = boto3.resource(
        'dynamodb',
        region_name=DESTINATION_REGION,
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    table = dynamodb_dest.Table(DESTINATION_TABLE_NAME)
    return table

def lambda_handler(event, context):
    table = assume_cross_account_role()
    print("Event received:", json.dumps(event))

    records = event.get('Records', [])
    if not records:
        print("No hay clave en los registros encontrados.")
        return

    for record in records:
        eventName = record['eventName']
        print(f"Event Type: {eventName}")

        try:
            if eventName in ['INSERT', 'MODIFY']:
                new_image = record['dynamodb']['NewImage']
                item = deserialize_dynamodb_item(new_image)
                table.put_item(
                    TableName=DESTINATION_TABLE_NAME,
                    Item=item
                )
                print("Deserialized Item:", item)
                print("Item replicado correctamente en tabla destino.")
            elif eventName == 'REMOVE':
                key = record['dynamodb']['Keys']
                deserialized_key = deserialize_dynamodb_item(key)
                table.delete_item(
                    TableName=DESTINATION_TABLE_NAME,
                    Key=deserialized_key
                )
                print("Item eliminado correctamente.")
        except Exception as e:
            print(f"Error replicando item: {str(e)}")