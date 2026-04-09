import pytest


def test_generate_pdf_success(auth_client_logged_in):
    response= auth_client_logged_in.post("/pdf/", json=
                          {"text":"## Day 1\nVist gampaha"})
    assert response.status_code==200
    assert response.headers["content-type"]=="application/pdf"


def test_pdf_empty_text(auth_client_logged_in):
    response= auth_client_logged_in.post("/pdf/", json=
                          {"text":""})
    assert response.status_code in [200,422]




