import os
import pytest
from backend import Backend

def test_process_request_creates_file():
    """
       Test if process_request creates an image file
       when given a valid KEGG pathway ID.
    """
    backend = Backend()

    # Use a  KEGG ID that usually works
    kegg_id = "hsa00010"
    output_file = "output/test_graph.png"

    # Run the function
    backend.process_request(kegg_id, output_file)

    # Check if the file was created
    assert os.path.exists(output_file)



def test_process_request_invalid_kegg_id():
    """
        Test if process_request raises an exception
        when given an invalid KEGG ID.
        Also checks that no file is created.
    """
    backend = Backend()

    bad_kegg_id = "invalid123"
    output_file = "should_not_exist.png"

    with pytest.raises(Exception):
        backend.process_request(bad_kegg_id, output_file)

    # Make sure the file was not created
    assert not os.path.exists(output_file)
