# 아키텍처 상세 설명

## 🏗️ 듀얼 모델 아키텍처 개요

이 프로젝트는 Amazon Bedrock의 Nova 모델 제품군을 활용하여 **"지연-품질 상충 관계"**를 해결하는 혁신적인 아키텍처를 구현합니다.

### 핵심 개념

```
사용자 질문
    ↓
┌─────────────────────────────────────┐
│        오케스트레이터                   │
│   (ThreadPoolExecutor)              │
└─────────────────────────────────────┘
    ↓                    ↓
┌─────────────┐    ┌─────────────┐
│ Nova Micro  │    │ Nova Pro    │
│ (단거리주자)   │    │ (장거리주자)   │
│ 즉시 응답     │    │ 상세 답변      │
└─────────────┘    └─────────────┘
    ↓                    ↓
┌─────────────┐    ┌─────────────┐
│ 초기 응답     │    │ 스트리밍      │
│ 표시         │    │ 답변 표시     │
└─────────────┘    └─────────────┘
```

## 🧠 모델별 역할 분석

### Nova Micro (단거리 주자)
- **목적**: 즉각적인 사용자 피드백 제공
- **특성**: 
  - TTFT (Time to First Token): ~0.33초
  - 처리량: ~210-386 tokens/s
  - 비용: 입력 $0.04/1M, 출력 $0.14/1M 토큰
- **역할**: 사용자 질문 인지 및 준비 중 알림

### Nova Pro (장거리 주자)
- **목적**: 고품질 상세 답변 생성
- **특성**:
  - 멀티모달 지원 (텍스트, 이미지, 비디오)
  - 컨텍스트 창: 300k 토큰
  - 비용: 입력 $0.80/1M, 출력 $3.20/1M 토큰
- **역할**: 전문가 수준의 포괄적 답변 제공

## ⚡ 병렬 처리 메커니즘

### ThreadPoolExecutor 선택 이유

1. **I/O 바운드 작업**: Bedrock API 호출은 네트워크 응답 대기
2. **구현 단순성**: 동기식 코드베이스에 쉽게 통합
3. **성능 효율성**: CPU 바운드가 아닌 I/O 바운드에 최적화

### 실행 흐름

```python
with ThreadPoolExecutor(max_workers=2) as executor:
    # 1. 두 작업을 동시에 시작
    future_micro = executor.submit(invoke_nova_micro, prompt)
    future_pro = executor.submit(stream_nova_pro, prompt)
    
    # 2. Nova Micro 결과 먼저 처리
    micro_result = future_micro.result()
    display_initial_response(micro_result)
    
    # 3. Nova Pro 스트림 처리
    pro_stream = future_pro.result()
    stream_detailed_response(pro_stream)
```

## 📡 스트리밍 처리 상세

### Bedrock 스트리밍 응답 구조

```json
{
  "contentBlockDelta": {
    "delta": {
      "text": "응답 텍스트 청크"
    },
    "contentBlockIndex": 0
  }
}
```

### 스트리밍 처리 로직

```python
for event in stream:
    chunk = event.get('chunk')
    if chunk:
        chunk_obj = json.loads(chunk.get('bytes').decode())
        if 'contentBlockDelta' in chunk_obj:
            delta = chunk_obj['contentBlockDelta'].get('delta', {})
            text_content = delta.get('text', '')
            if text_content:
                yield text_content
```

## 🎯 프롬프트 엔지니어링 전략

### 역할별 프롬프트 설계

#### Nova Micro 프롬프트
```
목적: 사용자 질문 인지 및 준비 중 알림
특징: 짧고 격려적인 한 문장
예시: "질문을 이해했으며, 상세한 답변을 준비하고 있습니다!"
```

#### Nova Pro 프롬프트
```
목적: 전문가 수준의 상세 답변
특징: 구조화된 형식, 마크다운 사용
예시: "다음 질문에 대해 전문가 수준의 상세하고 구조화된 답변을 제공해주세요..."
```

## 💰 비용 최적화 전략

### 비용 분석 모델

```python
# 일반적인 상호작용 비용
user_input_tokens = 50
micro_output_tokens = 30
pro_output_tokens = 500

micro_cost = (50/1_000_000 * 0.04) + (30/1_000_000 * 0.14)
pro_cost = (50/1_000_000 * 0.80) + (500/1_000_000 * 3.20)
total_cost = micro_cost + pro_cost  # ~$0.0016
```

### 최적화 포인트

1. **적재적소 활용**: 간단한 작업에는 저비용 모델
2. **토큰 제한**: 각 모델의 max_tokens 적절히 설정
3. **캐싱 활용**: 반복적인 질문에 대한 응답 캐싱 고려

## 🔧 확장성 고려사항

### 웹 애플리케이션 확장

```
Frontend (React/Vue)
    ↓ WebSocket
API Gateway WebSocket API
    ↓ Lambda Trigger
Lambda Function (Dual Model Logic)
    ↓ Bedrock API
Nova Micro + Nova Pro
```

### 마이크로서비스 아키텍처

```
┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │   Load Balancer │
└─────────────────┘    └─────────────────┘
         ↓                       ↓
┌─────────────────┐    ┌─────────────────┐
│ Orchestrator    │    │ Response Cache  │
│ Service         │    │ Service         │
└─────────────────┘    └─────────────────┘
         ↓
┌─────────────────┐    ┌─────────────────┐
│ Nova Micro      │    │ Nova Pro        │
│ Service         │    │ Service         │
└─────────────────┘    └─────────────────┘
```

## 🛡️ 오류 처리 및 복원력

### Fallback 전략

1. **Nova Micro 실패**: 즉시 Nova Pro 스트림으로 전환
2. **Nova Pro 실패**: Micro 응답 + 오류 메시지 표시
3. **네트워크 오류**: 재시도 로직 + 타임아웃 설정

### 모니터링 포인트

- API 호출 지연 시간
- 토큰 사용량
- 오류율
- 사용자 만족도 (응답 시간 기준)

## 📊 성능 메트릭

### 측정 지표

1. **TTFT (Time to First Token)**: 첫 응답까지의 시간
2. **Total Response Time**: 전체 응답 완료 시간
3. **Token Throughput**: 초당 토큰 생성 속도
4. **Cost per Interaction**: 상호작용당 비용

### 벤치마크 목표

- 초기 응답: < 2초
- 전체 응답: < 15초 (복잡한 질문 기준)
- 비용: < $0.002 per interaction
- 사용자 만족도: > 90%
