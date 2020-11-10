# AWS Python Lambda Template

## Local development

- Install the python version that you intend to use in the lambda function.
- Clone this repo

```
$ cd batch-trigger-lambda-template
```

- Define your parsing process in the function `process` inside parse/parse.py
- Create and activate virtual test environment by defining a test object in test_template.py
- Run tests using command below

```
$ python -m unittest -v
```

## Deploy function stack with cloudformation

- Install and configure the AWS CLI
- Navigate to the project directory
- Create code deployment package
```
$ zip function.zip *.py parse/*.py
```

- Create cloudformation stack
- Define parameters inside cloudformation.yml specific to your application
```
$ aws cloudformation create-stack --stack-name your-stack-name --template-body file://cloudformation.yml --capabilities CAPABILITY_IAM --capabilities CAPABILITY_NAMED_IAM
```

- Using the AWS console or cloudformation.yml find the name of your two created lambdas and use in the update function code below
- Deploy code package 

The function deploys with dummy code. Replace that code with the package that you created earlier.

```
$ aws lambda update-function-code --function-name {ParserName}-event --zip-file fileb://function.zip
$ aws lambda update-function-code --function-name {ParserName}-batch --zip-file fileb://function.zip
```

## Update function stack with cloudformation

- Create code deployment package
```
$ zip function.zip *.py parse/*.py
```

- Update cloudformation stack

```
$ aws cloudformation update-stack --stack-name your-stack-name --template-body file://cloudformation.yml --capabilities CAPABILITY_IAM --capabilities CAPABILITY_NAMED_IAM
```

The function deploys with dummy code. Replace that code with the package that you created earlier.

```
$ aws lambda update-function-code --function-name {ParserName}-event --zip-file fileb://function.zip
$ aws lambda update-function-code --function-name {ParserName}-batch --zip-file fileb://function.zip
```

