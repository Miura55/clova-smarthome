#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { ClovaIoThubStack } from '../lib/lambda-container-stack';
import { DefaultStackSynthesizer } from 'aws-cdk-lib';

const app = new cdk.App();
const fileAssetBucket = app.node.tryGetContext('fileAssetBucket');
new ClovaIoThubStack(app, 'ClovaIoThub', {
  synthesizer: new DefaultStackSynthesizer({
    fileAssetsBucketName: fileAssetBucket
  })
});
