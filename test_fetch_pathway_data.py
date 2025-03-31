import pytest
from backend import KEGGHandler
from unittest.mock import patch


def test_fetch_pathway_data_success():
    """This function tests the fetch_pathway_data method with a valid KEGG ID."""
    kegg_handler = KEGGHandler()
    kegg_id = "hsa00010"
    mock_response = "PATHWAY DATA FOR TESTING"

    with patch.object(kegg_handler.kegg, "get", return_value = mock_response):
        result = kegg_handler.fetch_pathway_data(kegg_id)
        assert result == mock_response


def test_fetch_pathway_data_exception():
    """This function tests the fetch_pathway_data method if an error occurs.
    """
    kegg_handler = KEGGHandler()
    kegg_id = "hsa00010"

    with patch.object(kegg_handler.kegg, "get", side_effect = Exception("API Error")):
        with pytest.raises(Exception, match = "Error fetching pathway data: API Error"):
            kegg_handler.fetch_pathway_data(kegg_id)


