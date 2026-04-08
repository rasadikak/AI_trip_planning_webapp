import pytest
from conftest import client

def test_generate_pdf_success(client):
    response= client.post("/pdf/", data=
                          {"text":"## Day 1\nVist gampaha"})
    assert response.status_code==200
    assert response.headers["media_type"]=="application/pdf"


def test_pdf_empty_text(client):
    response= client.post("/pdf/", data=
                          {"text":""})
    assert response.status_code in [200,422]




