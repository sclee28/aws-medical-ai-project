# Streamlit + FastAPI + Lambda 통합 설정

## 구조
- **Streamlit 앱**: 사용자 입력 폼 (`streamlit_app/app.py`)
- **FastAPI 백엔드**: Lambda 함수 호출 API (`fastapi_backend/main.py`)  
- **Lambda 함수**: 입력값을 처리하여 응답 (`simple-lambda-app/lambda/index.ts`)

## 설정 단계

### 1. Lambda 함수 배포
```bash
cd simple-lambda-app/
npm run build
npm run deploy
```

### 2. FastAPI 백엔드 실행
```bash
cd fastapi_backend/
pip install -r requirements.txt
export LAMBDA_FUNCTION_NAME="MyTaggableLambdaStack-MyFunctionXXXXXXXX"  # 실제 함수명으로 교체
python main.py
```

### 3. Streamlit 앱 실행
```bash
cd streamlit_app/
pip install -r requirements.txt
streamlit run app.py
```

## 사용법
1. Streamlit 웹 인터페이스에서 값 입력
2. "🚀 Invoke Lambda" 버튼 클릭
3. Lambda 함수 응답 확인

## 환경 변수
- `LAMBDA_FUNCTION_NAME`: Lambda 함수명
- `AWS_DEFAULT_REGION`: AWS 리전 (기본값: us-east-1)