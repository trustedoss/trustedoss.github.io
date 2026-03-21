"""
라이선스 혼재 시연용 샘플 앱.

이 모듈은 MIT, Apache-2.0, BSD, GPL 라이선스가 혼재된
의존성 패키지를 임포트하는 최소한의 예제입니다.
"""

import yaml          # PyYAML - MIT 라이선스
import requests      # requests - Apache-2.0 라이선스
import celery        # celery - BSD 라이선스

# mysql.connector 는 GPL-2.0 (Oracle MySQL Connector/Python)
# 임포트 시도 (설치된 경우에만 동작)
try:
    import mysql.connector  # mysql-connector-python - GPL-2.0
    print("mysql.connector 임포트 성공 (GPL-2.0 라이선스)")
except ImportError:
    print("mysql.connector 미설치 (실습 환경에서는 정상)")


def main():
    print("=== 라이선스 혼재 샘플 앱 ===")

    # PyYAML (MIT) 사용 예시
    data = yaml.safe_load("name: trustedoss\nversion: 1.0")
    print(f"YAML 파싱 결과 (MIT): {data}")

    # requests (Apache-2.0) 사용 예시
    print(f"requests 버전 (Apache-2.0): {requests.__version__}")

    # celery (BSD) 사용 예시
    print(f"celery 버전 (BSD): {celery.__version__}")

    print("\n경고: GPL 패키지(mysql-connector-python)가 포함되어 있습니다.")
    print("배포 방식에 따라 소스코드 공개 의무가 발생할 수 있습니다.")


if __name__ == "__main__":
    main()
