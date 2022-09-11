import { Stack, StackProps, CfnOutput } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import {
  DockerImageFunction,
  DockerImageCode,
  FunctionUrlAuthType,
  HttpMethod,
} from 'aws-cdk-lib/aws-lambda';
import * as dotenv from 'dotenv';

dotenv.config({ path: '../.env' });

export class ClovaIoThubStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const funcionApp = new DockerImageFunction(this, 'clova-iot-hub', {
      code: DockerImageCode.fromImageAsset('../lambda'),
      environment: {
        'BEEBOTTE_URL': process.env.BEEBOTTE_URL || '',
        'CLOVA_EXTENSION_ID': process.env.CLOVA_EXTENSION_ID || '',
      }
    });

    const funcitonUrl = funcionApp.addFunctionUrl({
      authType: FunctionUrlAuthType.NONE,
      cors: {
        allowedMethods: [HttpMethod.ALL],
        allowedOrigins: ['*'],
      } 
    });
    new CfnOutput(this, 'FunctionUrl', { value: funcitonUrl.url });
  }
}
