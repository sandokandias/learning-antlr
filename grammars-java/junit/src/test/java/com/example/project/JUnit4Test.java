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

import static org.junit.Assert.assertEquals;
import static java.lang.System.out;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;

public class JUnit4Test {

	private Calculator calculator;
	private Long startTime;

	@BeforeClass
	public static void beforeClass() {
		out.println("Test suite start.");
	}

	@AfterClass
	public static void afterClass() {
		out.println("Test suite end.");
	}

	@Before
	public void before() {
		calculator = new Calculator();
		startTime = System.currentTimeMillis();
	}

	@After
	public void after() {
		Long endTime = System.currentTimeMillis() - startTime;
		out.println("Test time (ms):" + endTime);
	}

	@Test
	public void testOnePlusTwo() {
		assertEquals(3, calculator.add(1, 2));
	}

	@Test(timeout = 1L)
	public void testThreePlusFour() {
		assertEquals(7, calculator.add(3, 4));
	}

	@Test(expected = ArithmeticException.class)
	public void testZeroDivision() {
		calculator.divide(0, 1);
	}

	@Ignore
	@Test
	public void testIgnore() {
		assertEquals(0, calculator.add(0, 0));
	}
}
