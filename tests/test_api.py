"""Tests for JokeAPI endpoints using Playwright's APIRequestContext."""

import pytest
from playwright.sync_api import APIRequestContext

from constants import JOKE_API_URL, LANGUAGES_ENDPOINT, LANGUAGE_CODE, DEFAULT_LANGUAGE, LANGUAGE_MAPPINGS, FLAGS_ENDPOINT, TIMESTAMP_LENGTH, EXPECTED_CONTENT_FLAGS
from enums import HttpStatusCodes, JokeCategories, JokeTypes, JokeLanguages, SystemLanguages


class TestJokeAPI:

    @pytest.mark.parametrize("category, expected_status, has_joke", [
        (JokeCategories.ANY, HttpStatusCodes.HTTP_OK, True),
        (JokeCategories.PROGRAMMING, HttpStatusCodes.HTTP_OK, True),
        (JokeCategories.DARK, HttpStatusCodes.HTTP_OK, True),
        (JokeCategories.MISC, HttpStatusCodes.HTTP_OK, True),
        (JokeCategories.NONEXISTING, HttpStatusCodes.HTTP_BAD_REQUEST, False),
    ])
    def test_get_joke_by_category(
        self,
        api_request_context: APIRequestContext,
        category: JokeCategories,
        expected_status: HttpStatusCodes,
        has_joke: bool
        ) -> None:
        """
        Get a joke by category.

        Args:
            api_request_context (APIRequestContext): The API request context.
            category (str): The joke category.
            expected_status (int): The expected HTTP status code.
            has_joke (bool): Whether a joke is expected in the response.

        Raises:
            AssertionError: If the test case fails.
        """
        response = api_request_context.get(f"joke/{category.value}")

        assert response.status == expected_status.value
        assert response.url == f"{JOKE_API_URL}joke/{category.value}"
        data = response.json()
        
        # Check error field exists and is boolean
        assert "error" in data, f"Category {category.value}: Missing 'error' field"
        assert isinstance(data["error"], bool), f"Category {category.value}: 'error' should be boolean"

        if expected_status == HttpStatusCodes.HTTP_OK:

            assert has_joke and not data["error"], f"Category {category.value}: Expected valid joke"
            assert "joke" in data or ("setup" in data and "delivery" in data)

            assert "type" in data, f"Category {category.value}: Missing 'type' field"
            assert data["type"] in [JokeTypes.SINGLE.value, JokeTypes.TWOPART.value], f"Category {category.value}: Invalid type '{data['type']}'"

            # Both single and twopart jokes should have either joke or setup+delivery
            if data["type"] == JokeTypes.SINGLE.value:
                assert "joke" in data, f"Category {category.value}: Single joke missing 'joke' field"
                assert isinstance(data["joke"], str) and data["joke"], f"Category {category.value}: 'joke' should be a non-empty string"

            elif data["type"] == JokeTypes.TWOPART.value:
                assert "setup" in data and "delivery" in data, f"Category {category.value}: Missing 'setup' or 'delivery' for twopart joke"
                assert isinstance(data["setup"], str) and data["setup"], f"Category {category.value}: 'setup' should be a non-empty string"
                assert isinstance(data["delivery"], str) and data["delivery"], f"Category {category.value}: 'delivery' should be a non-empty string"

        elif expected_status == HttpStatusCodes.HTTP_BAD_REQUEST:
            assert data["error"] is True, f"Category {category.value}: Expected error for invalid category"
            assert "message" in data, f"Category {category.value}: Missing error message"

        else:
            raise AssertionError(f"Unhandled expected status {expected_status.value} for category {category.value}")

    def test_get_languages(self, api_request_context: APIRequestContext) -> None:
        """
        Get all supported languages.
        
        Args:
            api_request_context (APIRequestContext): The API request context.
        """
        response = api_request_context.get(LANGUAGES_ENDPOINT)
        
        assert response.status == HttpStatusCodes.HTTP_OK.value
        data = response.json()
        
        # Validate response structure based on actual API response
        assert "defaultLanguage" in data
        assert data["defaultLanguage"] == DEFAULT_LANGUAGE
        
        assert "jokeLanguages" in data
        assert isinstance(data["jokeLanguages"], list)
        assert len(data["jokeLanguages"]) > 0
        
        expected_joke_languages = [lang.value for lang in JokeLanguages]
        for lang in expected_joke_languages:
            assert lang in data["jokeLanguages"], f"Expected language '{lang}' not found in jokeLanguages"
        
        assert set(data["jokeLanguages"]) == set(expected_joke_languages), \
            f"Joke languages mismatch. Expected: {expected_joke_languages}, Got: {data['jokeLanguages']}"
        
        assert "systemLanguages" in data  
        assert isinstance(data["systemLanguages"], list)
        assert len(data["systemLanguages"]) > 0
        
        # Validate system languages contain at least some expected ones
        expected_system_languages = [lang.value for lang in SystemLanguages]
        for lang in expected_system_languages:
            assert lang in data["systemLanguages"], f"Expected system language '{lang}' not found"
        
        assert "possibleLanguages" in data
        assert isinstance(data["possibleLanguages"], list)
        assert len(data["possibleLanguages"]) > 0
        
        
    @pytest.mark.parametrize("language_name, expected_code", list(LANGUAGE_MAPPINGS.items()))
    def test_get_language_code(
        self,
        api_request_context: APIRequestContext,
        language_name: str,     
        expected_code: str
    ) -> None:
        """
        Get ISO language code from language name
        
        Args:
            api_request_context (APIRequestContext): The API request context.
            language_name (str): The name of the language.
            expected_code (str): The expected ISO language code.
        """
        response = api_request_context.get(f"{LANGUAGE_CODE}/{language_name}")

        assert response.status == HttpStatusCodes.HTTP_OK.value
        data = response.json()
        assert data["error"] is False
        assert "code" in data
        assert data["code"] == expected_code

    def test_get_flags(self, api_request_context: APIRequestContext) -> None:
        """
        Get available blacklist flags.

        Args:
            api_request_context (APIRequestContext): The API request context.
        """
        response = api_request_context.get(FLAGS_ENDPOINT)
        assert response.status == HttpStatusCodes.HTTP_OK.value, f"Expected {HttpStatusCodes.HTTP_OK.value}, got {response.status}"
        data = response.json()
        
        # Validate response structure
        assert "flags" in data, "Missing 'flags' field"
        assert isinstance(data["flags"], list), "'flags' should be a list/array"
        assert len(data["flags"]) > 0, "'flags' array should not be empty"
        
        # Validate timestamp exists and is correct format (13-character UNIX timestamp)
        assert "timestamp" in data, "Missing 'timestamp' field"
        assert isinstance(data["timestamp"], int), "Timestamp should be an integer"
        
        # Convert to string to check length (13-character requirement)
        timestamp_str = str(data["timestamp"])
        assert len(timestamp_str) == TIMESTAMP_LENGTH, f"Timestamp should be {TIMESTAMP_LENGTH} characters, got {len(timestamp_str)}"
        
        # Validate flag structure - each flag should be a string
        for flag in data["flags"]:
            assert isinstance(flag, str), f"Each flag should be a string, got {type(flag)}"
            assert len(flag) > 0, "Flag should not be empty"
        
        # Check that common expected flags are present
        for expected_flag in EXPECTED_CONTENT_FLAGS:
            assert expected_flag in data["flags"], f"Expected flag '{expected_flag}' not found in flags list"


    # @pytest.mark.parametrize("joke_type, category, use_dry_run", [
    #     ("single", "Programming", True),   # Test dry-run with single joke
    #     ("twopart", "Dark", True),         # Test dry-run with twopart joke  
    #     ("single", "Misc", False),         # Test actual submission (if allowed)
    # ])
    # def test_submit_joke(
    #     self,
    #     api_request_context: APIRequestContext,
    #     joke_type: str,
    #     category: str,
    #     use_dry_run: bool
    # ) -> None:
    #     """
    #     Submit a new joke (with dry-run option)

    #     Args:
    #         api_request_context (APIRequestContext): The API request context.
    #         joke_type (str): Type of joke ("single" or "twopart").
    #         category (str): Joke category.
    #         use_dry_run (bool): Whether to use dry-run mode.
    #     """
    #     # Prepare flags object (required by API)
    #     flags = {
    #         "nsfw": False,
    #         "religious": False, 
    #         "political": False,
    #         "racist": False,
    #         "sexist": False,
    #         "explicit": False
    #     }
        
    #     # Prepare joke payload based on type
    #     if joke_type == "single":
    #         payload = {
    #             "formatVersion": 3,
    #             "category": category,
    #             "type": "single",
    #             "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    #             "flags": flags,
    #             "lang": "en"
    #         }
    #     else:  # twopart
    #         payload = {
    #             "formatVersion": 3,
    #             "category": category,
    #             "type": "twopart",
    #             "setup": "Why did the skeleton go to the party?",
    #             "delivery": "Because he wanted to have a bone-chilling time!",
    #             "flags": flags,
    #             "lang": "en"
    #         }
        
    #     # Construct URL with dry-run parameter if needed
    #     endpoint = "submit"
    #     if use_dry_run:
    #         endpoint += "?dry-run"
        
    #     # Send POST request with JSON payload
    #     response = api_request_context.post(
    #         endpoint,
    #         data=payload,
    #         headers={"Content-Type": "application/json"}
    #     )
        
    #     # Validate response
    #     assert response.status == 201, f"Expected 201 (Created), got {response.status}"
        
    #     data = response.json()
        
    #     # Validate response structure
    #     if "error" in data:
    #         assert data["error"] is False, f"Submission failed with error: {data.get('message', 'Unknown error')}"
        
    #     # For dry-run, expect confirmation without actual submission
    #     if use_dry_run:
    #         # Dry-run should validate the joke but not save it
    #         assert "message" in data or "status" in data, "Expected dry-run confirmation message"
    #     else:
    #         # Actual submission should return submission ID or confirmation
    #         assert "submissionID" in data or "id" in data or "message" in data, \
    #             "Expected submission confirmation with ID"