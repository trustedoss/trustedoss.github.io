package com.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Sample app for practising detection of CVE-2021-44228 (Log4Shell).
 *
 * It deliberately uses the vulnerable log4j-core 2.14.1.
 * Do not use it to attack anything. It exists for training only.
 */
public class App {

    private static final Logger logger = LogManager.getLogger(App.class);

    public static void main(String[] args) {
        logger.info("Application started");
        logger.info("Hello, World!");
        logger.info("This app uses log4j-core 2.14.1, the version affected by CVE-2021-44228");
        logger.warn("Warning: this version carries the Log4Shell vulnerability (CVSS 10.0, Critical)");
        logger.info("Fix: change the log4j-core version in pom.xml to 2.17.1 or later");
    }
}
