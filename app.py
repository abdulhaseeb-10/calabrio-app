#!/usr/bin/env python3
import os
import aws_cdk as cdk
from calabrio_app.calabrio_app import CalabrioApp

app = cdk.App()
CalabrioApp(app, "CalabrioApp")
app.synth()