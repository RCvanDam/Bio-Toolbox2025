import pytest
from unittest.mock import patch, Mock
from backend import GeneHandler  # Import the GeneHandler class from backend.py

# Define test data for gene names, species, and expected results
GENES = ["BRCA1", "TP53"]
SPECIES = "hsa"  # Human species code for KEGG
KEGG_IDS = {"BRCA1": "hsa:101", "TP53": "hsa:102"}  # Expected KEGG IDs for the given genes
PATHWAY_IDS = {"hsa:101": ["path:hsa04110", "path:hsa04115"], "hsa:102": ["path:hsa05210"]}  # Expected pathway mappings


@pytest.fixture
def gene_handler():
    """
    Pytest fixture to initialize the GeneHandler object with test data.
    This ensures that the setup is reusable across multiple tests.
    """
    return GeneHandler(GENES, SPECIES)


@patch("backend.requests.get")  # Mock the requests.get function to avoid actual API calls
def test_get_kegg_ids(mock_get, gene_handler):
    """
    Test the get_kegg_ids method of the GeneHandler class.
    This verifies that the method correctly retrieves KEGG IDs for the given genes.
    """
    # Simulate a successful API response for KEGG ID retrieval
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = (
        "hsa:101\tBRCA1 description\n"  # Simulated response for BRCA1
        "hsa:102\tTP53 description\n"   # Simulated response for TP53
    )
    mock_get.return_value = mock_response  # Use the mocked response

    # Call the method and check the output
    result = gene_handler.get_kegg_ids()

    # Assertions: Verify the result matches the expected KEGG IDs
    assert result == KEGG_IDS
    # Ensure that the correct API calls were made for each gene
    mock_get.assert_any_call(f"http://rest.kegg.jp/find/genes/BRCA1")
    mock_get.assert_any_call(f"http://rest.kegg.jp/find/genes/TP53")


@patch("backend.requests.get")
def test_get_pathway_ids(mock_get, gene_handler):
    """
    Test the get_pathway_ids method of the GeneHandler class.
    This verifies that the method retrieves the correct pathway IDs for given KEGG IDs.
    """
    # Simulate a successful API response for pathway retrieval
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = (
        "PATHWAY  hsa04110\tCell cycle\n"  # Example pathway for KEGG ID 101
        "PATHWAY  hsa04115\tp53 signaling\n"  # Additional pathway for KEGG ID 101
    )
    mock_get.return_value = mock_response  # Use the mocked response

    # Call the method and check the output
    result = gene_handler.get_pathway_ids(KEGG_IDS.values())

    # Assertions: Verify the result matches the expected pathways
    assert result == PATHWAY_IDS
    # Ensure the correct API calls were made for each KEGG ID
    for kegg_id in KEGG_IDS.values():
        mock_get.assert_any_call(f"http://rest.kegg.jp/get/{kegg_id}")
