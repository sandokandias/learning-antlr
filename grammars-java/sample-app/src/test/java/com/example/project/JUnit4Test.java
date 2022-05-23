/*
 * Copyright 2015-2021 the original author or authors.
 *
 * All rights reserved. This program and the accompanying materials are
 * made available under the terms of the Eclipse Public License v2.0 which
 * accompanies this distribution and is available at
 *
 * http://www.eclipse.org/legal/epl-v20.html
 */
package com.example.project;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static java.lang.System.out;
import org.junit.jupiter.api.Timeout;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;

public class JUnit4Test {

        private Calculator calculator;
        private Long startTime;

        @BeforeAll
        public static void beforeClass() {
                out.println("Test suite start.");
        }

        @AfterAll
        public static void afterClass() {
                out.println("Test suite end.");
        }

        @BeforeEach
        public void before() {
                calculator = new Calculator();
                startTime = System.currentTimeMillis();
        }

        @AfterEach
        public void after() {
                Long endTime = System.currentTimeMillis() - startTime;
                out.println("Test time (ms):" + endTime);
        }

        @Test
        public void testOnePlusTwo() {
                assertEquals(3, calculator.add(1, 2));
        }

        @Test
        @Timeout(1)
        public void testThreePlusFour() {
                assertEquals(7, calculator.add(3, 4));
        }

        @Test
        public void testZeroDivision() {
                assertThrows(ArithmeticException.class, () -> {
                        calculator.divide(1, 0);
                });
        }

        @Disabled
        @Test
        public void testIgnore() {
                assertEquals(0, calculator.add(0, 0));
        }
}