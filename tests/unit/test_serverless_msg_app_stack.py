import aws_cdk as core
import aws_cdk.assertions as assertions

from calabrio_app.calabrio_app import CalabrioApp

def test_sqs_queue_created():
    app = core.App()
    stack = CalabrioApp(app, "serverless-msg-app")
    template = assertions.Template.from_stack(stack)