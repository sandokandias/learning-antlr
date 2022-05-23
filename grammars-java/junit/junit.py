annotations = {
    "@Before": "@BeforeEach",
    "@After": "@AfterEach",
    "@BeforeClass": "@BeforeAll",
    "@AfterClass": "@AfterAll",
    "@Ignore": "@Disabled"
}

imports = {
    "org.junit.After": "org.junit.jupiter.api.AfterEach",
    "org.junit.Before": "org.junit.jupiter.api.BeforeEach",
    "org.junit.AfterClass": "org.junit.jupiter.api.AfterAll",
    "org.junit.BeforeClass": "org.junit.jupiter.api.BeforeAll",
    "org.junit.Ignore": "org.junit.jupiter.api.Disabled",
    "org.junit.Test": "org.junit.jupiter.api.Test",
    "org.junit.Assert.assertEquals": "org.junit.jupiter.api.Assertions.assertEquals",
    "expected": "import static org.junit.jupiter.api.Assertions.assertThrows;",
    "timeout": "import org.junit.jupiter.api.Timeout;"
}

expected_lambda = ("import static org.junit.jupiter.api.Assertions.assertThrows;","\n\t\tassertThrows(@exception, () -> {", "\t});\n\t")