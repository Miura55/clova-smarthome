import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class ClovaIoThubStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    new lambda.DockerImageFunction(this, 'clova-iot-hub', {
      code: lambda.DockerImageCode.fromImageAsset('../lambda'),
    })
  }
}
