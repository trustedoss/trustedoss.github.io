package com.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * CVE-2021-44228 (Log4Shell) 취약점 탐지 실습용 샘플 앱.
 *
 * 이 코드는 취약한 log4j-core 2.14.1을 사용합니다.
 * 실제 공격에 사용하지 마세요. 교육 목적으로만 사용하세요.
 */
public class App {

    private static final Logger logger = LogManager.getLogger(App.class);

    public static void main(String[] args) {
        logger.info("애플리케이션 시작");
        logger.info("Hello, World!");
        logger.info("이 앱은 log4j-core 2.14.1을 사용합니다 (CVE-2021-44228 취약 버전)");
        logger.warn("경고: 이 버전은 Log4Shell 취약점(CVSS 10.0 Critical)이 존재합니다.");
        logger.info("수정 방법: pom.xml 에서 log4j-core 버전을 2.17.1 이상으로 변경하세요.");
    }
}
