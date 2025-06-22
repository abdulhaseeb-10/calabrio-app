from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from constructs import Construct
import os

class CalabrioApp(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #  DynamoDB Table
        self.table = dynamodb.Table(
            self, "MessagesTable",
            partition_key=dynamodb.Attribute(
                name="messageUUID",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        #  Lambda Function
        lambda_fn = DockerImageFunction(
            self, "MessageProcessorFunction",
            code=DockerImageCode.from_image_asset(os.path.join(os.getcwd(), "lambda_fn")),
            environment={
                "TABLE_NAME": self.table.table_name
            },
        )

        #  Add Permissions
        self.table.grant_write_data(lambda_fn)
        #  API Gateway (Invoke-HTTP)
        api = apigw.LambdaRestApi(
            self, "MessageApi",
            handler=lambda_fn,
            proxy=False
        )

        # Configure POST
        messages = api.root.add_resource("submit")
        messages.add_method("POST")