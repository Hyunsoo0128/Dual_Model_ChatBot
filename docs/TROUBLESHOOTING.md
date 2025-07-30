# 문제 해결 가이드

## 🚨 일반적인 문제 및 해결 방법

### 1. 모델 접근 권한 오류

#### 오류 메시지
```
botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the InvokeModel operation: You don't have access to the model with the specified model ID.
```

#### 해결 방법
1. **AWS Management Console 접속**
   - AWS Console에 로그인
   - Amazon Bedrock 서비스로 이동

2. **모델 접근 권한 활성화**
   ```
   Bedrock Console → Model access → Manage model access
   ```
   - ✅ Amazon Nova Micro 체크
   - ✅ Amazon Nova Pro 체크
   - "Save changes" 클릭

3. **권한 적용 확인**
   ```bash
   python test_nova_models.py
   ```

#### 추가 참고사항
- 모델 접근 권한 활성화는 계정당 한 번만 필요
- 일부 리전에서는 Nova 모델이 아직 지원되지 않을 수 있음
- 권한 활성화 후 몇 분 정도 대기 시간이 필요할 수 있음

---

### 2. AWS 자격 증명 오류

#### 오류 메시지
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

#### 해결 방법

##### 방법 1: AWS CLI 설정
```bash
# AWS CLI 설치
pip install awscli

# 자격 증명 설정
aws configure
```

입력 정보:
- AWS Access Key ID: `AKIA...`
- AWS Secret Access Key: `...`
- Default region name: `us-east-1`
- Default output format: `json`

##### 방법 2: 환경 변수 설정
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

##### 방법 3: 자격 증명 파일 생성
파일 위치: `~/.aws/credentials`
```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
region = us-east-1
```

#### 자격 증명 확인
```bash
aws sts get-caller-identity
```

---

### 3. 리전 관련 오류

#### 오류 메시지
```
botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL
```

#### 해결 방법
1. **지원 리전 확인**
   - Nova 모델은 특정 리전에서만 지원
   - 주로 `us-east-1` (N. Virginia)에서 지원

2. **리전 변경**
   ```python
   # nova_dual_chatbot.py에서
   chatbot = NovaDualChatbot(region='us-east-1')
   ```

3. **AWS CLI 리전 설정**
   ```bash
   aws configure set region us-east-1
   ```

---

### 4. 네트워크 및 타임아웃 오류

#### 오류 메시지
```
botocore.exceptions.ReadTimeoutError: Read timeout on endpoint URL
```

#### 해결 방법
1. **타임아웃 설정 증가**
   ```python
   config = Config(
       read_timeout=120,  # 기본 60초에서 120초로 증가
       connect_timeout=20,  # 기본 10초에서 20초로 증가
       retries={'max_attempts': 5}  # 재시도 횟수 증가
   )
   ```

2. **네트워크 연결 확인**
   ```bash
   ping bedrock-runtime.us-east-1.amazonaws.com
   ```

3. **방화벽/프록시 설정 확인**
   - 기업 네트워크의 경우 AWS 엔드포인트 접근 허용 필요

---

### 5. Python 환경 관련 오류

#### 오류 메시지
```
ModuleNotFoundError: No module named 'boto3'
```

#### 해결 방법
1. **가상 환경 생성 및 활성화**
   ```bash
   python -m venv nova_chatbot_env
   source nova_chatbot_env/bin/activate  # macOS/Linux
   # 또는
   nova_chatbot_env\Scripts\activate     # Windows
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **Python 버전 확인**
   ```bash
   python --version  # 3.8 이상 필요
   ```

---

### 6. 스트리밍 응답 문제

#### 증상
- Nova Pro 응답이 표시되지 않음
- 스트리밍이 중단됨

#### 해결 방법
1. **스트리밍 구조 확인**
   ```python
   # 디버깅용 코드 추가
   for event in stream:
       chunk = event.get('chunk')
       if chunk:
           chunk_obj = json.loads(chunk.get('bytes').decode())
           print(f"청크 구조: {chunk_obj}")  # 디버깅
   ```

2. **버퍼링 문제 해결**
   ```python
   sys.stdout.write(chunk)
   sys.stdout.flush()  # 즉시 출력 보장
   ```

---

### 7. 성능 관련 문제

#### 증상
- 응답 시간이 너무 느림
- 비용이 예상보다 높음

#### 해결 방법
1. **토큰 수 최적화**
   ```python
   "inferenceConfig": {
       "max_new_tokens": 100,  # Nova Micro는 짧게
       "max_new_tokens": 1000, # Nova Pro는 적절히
   }
   ```

2. **프롬프트 최적화**
   - 불필요한 설명 제거
   - 명확하고 간결한 지시사항

3. **병렬 처리 확인**
   ```python
   # ThreadPoolExecutor가 제대로 작동하는지 확인
   with ThreadPoolExecutor(max_workers=2) as executor:
       print("병렬 처리 시작")
   ```

---

## 🔍 디버깅 도구

### 1. 상세 로깅 활성화
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 응답 시간 측정
```python
import time

start_time = time.time()
# API 호출
end_time = time.time()
print(f"응답 시간: {end_time - start_time:.2f}초")
```

### 3. 토큰 사용량 모니터링
```python
# 응답에서 토큰 사용량 확인
if 'amazon-bedrock-invocationMetrics' in response:
    metrics = response['amazon-bedrock-invocationMetrics']
    print(f"입력 토큰: {metrics['inputTokenCount']}")
    print(f"출력 토큰: {metrics['outputTokenCount']}")
```

---

## 📞 추가 지원

### AWS 공식 문서
- [Amazon Bedrock 사용자 가이드](https://docs.aws.amazon.com/bedrock/)
- [Nova 모델 문서](https://docs.aws.amazon.com/bedrock/latest/userguide/nova-models.html)
- [Boto3 문서](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

### 커뮤니티 지원
- [AWS re:Post](https://repost.aws/)
- [GitHub Issues](https://github.com/your-username/amazon-nova-dual-chatbot/issues)

### 문제 보고
문제가 지속되면 다음 정보와 함께 이슈를 등록해주세요:
- 오류 메시지 전문
- Python 버전
- boto3 버전
- AWS 리전
- 실행 환경 (OS, 네트워크 등)
