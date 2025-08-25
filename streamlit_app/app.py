import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Lambda Invoker",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Lambda Function Invoker")
st.markdown("Enter a value and click the button to invoke your AWS Lambda function via FastAPI")

FASTAPI_URL = st.text_input(
    "FastAPI Backend URL", 
    value="http://localhost:8000",
    help="URL of your FastAPI backend server"
)

input_value = st.text_input(
    "Input Value", 
    placeholder="Enter any text here...",
    help="This value will be sent to your Lambda function"
)

if st.button("🚀 Invoke Lambda", type="primary"):
    if not input_value.strip():
        st.error("Please enter a value before invoking the Lambda function")
    elif not FASTAPI_URL.strip():
        st.error("Please enter the FastAPI backend URL")
    else:
        with st.spinner("Invoking Lambda function..."):
            try:
                response = requests.post(
                    f"{FASTAPI_URL.rstrip('/')}/invoke-lambda",
                    json={"value": input_value},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Lambda function invoked successfully!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📤 Input Sent")
                        st.code(result.get("input_received", "N/A"))
                    
                    with col2:
                        st.subheader("📥 Lambda Response")
                        lambda_response = result.get("lambda_response", {})
                        st.code(json.dumps(lambda_response, indent=2))
                        
                else:
                    st.error(f"❌ Error: {response.status_code}")
                    st.code(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to FastAPI backend. Make sure it's running!")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The Lambda function might be taking too long.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

st.markdown("---")
st.markdown("### 💡 Instructions")
st.markdown("""
1. Make sure your FastAPI backend is running (`python fastapi_backend/main.py`)
2. Enter the correct FastAPI backend URL (default: http://localhost:8000)
3. Enter any text value you want to send to the Lambda function
4. Click the "🚀 Invoke Lambda" button
5. View the response from your Lambda function below
""")