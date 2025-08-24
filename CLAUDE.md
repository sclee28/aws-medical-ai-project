# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AWS CDK project generated with Projen, containing a simple Lambda function deployment. The repository uses a multi-directory structure with the main CDK application in `simple-lambda-app/`.

## Architecture

- **CDK Stack**: `MyLambdaStack` in `src/main.ts` creates a Lambda function with tagging
- **Lambda Function**: Simple Node.js handler in `lambda/index.ts` returns a basic JSON response
- **IAM Integration**: Uses existing IAM role (pre-created) rather than creating new roles
- **Build System**: Projen manages all configuration and build processes

## Common Commands

Navigate to `simple-lambda-app/` directory first for all operations:

```bash
cd simple-lambda-app/
```

### Development
- `npm run build` - Compile TypeScript and run tests
- `npm run test` - Run Jest tests with coverage
- `npm run test:watch` - Run tests in watch mode
- `npm run eslint` - Run ESLint linting

### CDK Operations
- `npm run synth` - Synthesize CloudFormation templates
- `npm run diff` - Compare deployed stack with current state
- `npm run deploy` - Deploy stack to AWS
- `npm run destroy` - Destroy deployed stack

### Projen Management
- `npm run projen` - Regenerate project files from `.projenrc.ts`
- `npx projen new awscdk-app-ts` - Initialize new CDK app (as noted in main README)

## Testing

Tests use Jest with snapshot testing for CDK templates. Test files are in `test/` directory and coverage reports are generated in `coverage/`.

## Key Files

- `.projenrc.ts` - Projen configuration defining project structure
- `src/main.ts` - Main CDK stack definition
- `lambda/index.ts` - Lambda function source code
- `test/main.test.ts` - CDK stack tests

## Notes

- Project uses CDK v2 with TypeScript
- All npm scripts are Projen-managed - modify `.projenrc.ts` instead of `package.json` directly
- Lambda function references existing IAM role ARN `arn:aws:iam::666803869796:role/service-role/usgetypedontdelete-role-i0kicyiu`
- Stack applies `project: pre-1team` tag to all resources