# Auto-Chat-Classification-and-Answers-for-Live-Commerce

## 1. AWS S3 버킷 만들기 및 모델 파일 업로드

1. AWS S3 Bucket 생성 시, 모든 Public Access 차단을 비활성화 해줍니다.
2. 모델의 압축 파일 을 생성한 S3 버킷에 업로드 합니다.

## 2. AWS SageMaker 노트북 인스턴스 생성 및 모델 배포

1. AWS SageMaker 서비스의 노트북 인스턴스를 생성합니다.
2. 노트북 인스턴스 생성 시, IAM 역할 생성에서 특정 S3 버킷 항목을 선택 및 1번에서 생성한 S3 버킷의 이름을 입력해줍니다.

3. 생성된 노트북 인스턴스의 “Jupyter 열기” 를 통해서, 노트북 인스턴스에 접속합니다.
4. Repository 의 SageMaker.ipynb 파일의 Notebook에 해당하는 내용을 노트북 인스턴스에 입력 후 실행합니다.

## 3. AWS 의 Lambda 및 API Gateway 를 통한 API 생성

1. AWS Lambda 서비스를 생성 및 SageMaker.ipynb 파일의 Lamda에 해당하는 내용을 Lambda 서비스 코드에 입력합니다.
    - Lambda 생성 시, SageMaker 에 대한 Invoke Endpoint 의 권한을 추가시켜줍니다.
2. API Gateway 를 생성 및 AWS Lambda 서비스와 연결합니다.
    - 배포 Stage Name : chat-classify
    - 생성 API Method : POST
    - 생성 API : /classify
