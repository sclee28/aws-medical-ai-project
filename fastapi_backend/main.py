# 필요한 라이브러리들을 임포트합니다.
import json
import boto3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# FastAPI 애플리케이션을 생성합니다.
app = FastAPI(title="Lambda Invoker API", version="1.0.0")

# CORS(Cross-Origin Resource Sharing) 미들웨어를 추가합니다.
# 이 설정은 모든 외부 도메인(*)에서 이 API에 접근할 수 있도록 허용합니다.
# 이는 보통 개발 단계에서 편리하며, 프로덕션 환경에서는 특정 도메인만 허용하도록 변경해야 합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 출처(origin)를 허용
    allow_credentials=True, # 쿠키 등 자격 증명 허용
    allow_methods=["*"], # 모든 HTTP 메소드(GET, POST 등) 허용
    allow_headers=["*"], # 모든 HTTP 헤더 허용
)

# boto3 라이브러리를 사용하여 AWS Lambda 클라이언트를 초기화합니다.
# AWS 리전 정보는 환경 변수 'AWS_DEFAULT_REGION'에서 가져오고, 없으면 'ap-northeast-2'를 기본값으로 사용합니다.
lambda_client = boto3.client('lambda', region_name=os.getenv('AWS_DEFAULT_REGION', 'ap-northeast-2'))

# Pydantic을 사용하여 API 요청 바디의 데이터 모델을 정의합니다.
# 이 API는 'value'라는 문자열 필드를 가진 JSON 객체를 받습니다.
class InputData(BaseModel):
    value: str

# POST 요청을 처리하는 API 엔드포인트를 정의합니다.
# URL 경로는 "/invoke-lambda"이며, 비동기 함수로 정의됩니다.
@app.post("/invoke-lambda")
async def invoke_lambda(data: InputData):
    try:
        # 호출할 AWS Lambda 함수의 이름을 환경 변수에서 가져옵니다.
        # 환경 변수가 없을 경우 'say1-1team-llm-report'를 기본값으로 사용합니다.
        function_name = os.getenv('LAMBDA_FUNCTION_NAME', 'say1-1team-llm-report')
        
        # Lambda 함수에 전달할 페이로드(payload)를 구성합니다.
        # 이 페이로드는 API Gateway 프록시 통합을 시뮬레이션하기 위한 형식으로,
        # 'body'와 'httpMethod' 필드를 포함합니다.
        payload = {
            "body": json.dumps({"input_value": data.value}), # Lambda가 받을 실제 입력 값
            "httpMethod": "POST" # 요청 메소드
        }
        
        # boto3를 사용하여 AWS Lambda 함수를 호출합니다.
        # InvocationType='RequestResponse'는 동기 호출을 의미하며,
        # Lambda 함수가 실행을 완료하고 응답을 반환할 때까지 기다립니다.
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        # Lambda 함수의 응답 페이로드를 읽고 JSON으로 파싱합니다.
        response_payload = json.loads(response['Payload'].read())
        
        # 클라이언트에게 최종 응답을 반환합니다.
        # 호출 상태, Lambda 함수의 응답, 그리고 받은 입력 값을 포함합니다.
        return {
            "status": "success",
            "lambda_response": response_payload,
            "input_received": data.value
        }
        
    except Exception as e:
        # 예외 발생 시, 500 상태 코드와 함께 오류 메시지를 반환합니다.
        raise HTTPException(status_code=500, detail=f"Lambda invocation failed: {str(e)}")

# GET 요청을 처리하는 상태 확인(Health Check) 엔드포인트를 정의합니다.
# 이 엔드포인트를 통해 API가 정상적으로 작동하는지 확인할 수 있습니다.
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 이 스크립트가 직접 실행될 때만 uvicorn 서버를 실행합니다.
if __name__ == "__main__":
    import uvicorn
    # uvicorn을 사용하여 FastAPI 앱을 0.0.0.0 호스트의 8000 포트에서 실행합니다.
    # 0.0.0.0은 모든 네트워크 인터페이스에서 접근을 허용한다는 의미입니다.
    uvicorn.run(app, host="0.0.0.0", port=8000)