import pytest
from unittest.mock import patch, Mock
from backend import PathwayGenerator  # Import the PathwayGenerator class from backend.py
import os


@pytest.fixture
def pathway_generator():
    """
    Pytest fixture to initialize the PathwayGenerator object.
    This ensures the setup is reusable across multiple tests.
    """
    return PathwayGenerator()


@patch("backend.requests.get")
def test_save_pathway_image(mock_get, pathway_generator, tmp_path):
    """
    Test the save_pathway method when the response is a valid PNG image.
    This verifies that pathway images are correctly saved to the output folder.
    """
    # Simulate a successful API response with PNG content
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "image/png"}  # Response header indicates PNG content
    mock_response.iter_content = lambda chunk_size: [b"testimagechunk"]  # Simulated image content
    mock_get.return_value = mock_response  # Use the mocked response

    # Define test parameters
    pathway_id = "hsa04137"  # Example pathway ID
    output_folder = tmp_path  # Use pytest's temporary directory for testing
    pathway_generator.save_pathway(pathway_id, [], output_folder)  # Call the method

    # Assertions: Check that the PNG file was saved
    expected_file_path = os.path.join(output_folder, f"{pathway_id}.png")
    assert os.path.exists(expected_file_path)  # Verify the file exists
    with open(expected_file_path, "rb") as f:
        content = f.read()
    assert content == b"testimagechunk"  # Verify the file content matches the mocked response


@patch("backend.requests.get")
def test_save_pathway_fallback_to_text(mock_get, pathway_generator, tmp_path):
    """
    Test the save_pathway method when the response is not an image.
    This verifies the fallback behavior where the response is saved as a text file.
    """
    # Simulate a successful API response with non-image content
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/plain"}  # Response header indicates text content
    mock_response.text = "This is a fallback pathway description."  # Simulated text content
    mock_get.return_value = mock_response  # Use the mocked response

    # Define test parameters
    pathway_id = "hsa04137"  # Example pathway ID
    output_folder = tmp_path  # Use pytest's temporary directory for testing
    pathway_generator.save_pathway(pathway_id, [], output_folder)  # Call the method

    # Assertions: Check that the text file was saved
    expected_file_path = os.path.join(output_folder, f"{pathway_id}.txt")
    assert os.path.exists(expected_file_path)  # Verify the file exists
    with open(expected_file_path, "r") as f:
        content = f.read()
    assert content == "This is a fallback pathway description."  # Verify the file content matches the mocked response


@patch("backend.requests.get")
def test_save_pathway_error_handling(mock_get, pathway_generator, tmp_path):
    """
    Test the save_pathway method when an exception occurs during the request.
    This verifies the error-handling behavior and checks that the error is logged to a file.
    """
    # Simulate a network exception
    mock_get.side_effect = Exception("Network Error")  # Raise an exception for the mocked request

    # Define test parameters
    pathway_id = "hsa04137"  # Example pathway ID
    output_folder = tmp_path  # Use pytest's temporary directory for testing
    pathway_generator.save_pathway(pathway_id, [], output_folder)  # Call the method

    # Assertions: Check that the error file was created
    expected_file_path = os.path.join(output_folder, f"{pathway_id}_error.txt")
    assert os.path.exists(expected_file_path)  # Verify the file exists
    with open(expected_file_path, "r") as f:
        content = f.read()
    assert "Error retrieving pathway map: Network Error" in content  # Verify the error message matches
