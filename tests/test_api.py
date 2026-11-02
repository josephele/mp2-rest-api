def test_upload_csv(client, sample_csv_bytes):
    # TODO: Upload the sample CSV to POST /upload.
    # Assert status 200, six rows, two columns,
    # and a positive integer dataset ID.
    response = client.post(
        "/upload",
        files={"file": ("sample_data.csv", sample_csv_bytes, "text/csv")}
    )
    assert response.status_code == 200
    assert response.json()["rows"] == 6
    assert response.json()["columns"] == 2
    assert type(response.json()["id"]) == int
    assert response.json()["id"] > 0


def test_process_and_retrieve(
    client, uploaded_dataset_id, processing_body
):
    # TODO 1: Send a POST request to
    # /datasets/{uploaded_dataset_id}/process
    # using json=processing_body.
    # Assert status 200, one validation removal,
    # and a cleaning report showing 5 → 3 rows.
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body
    )
    assert response.status_code == 200
    assert response.json()["validation_rows_removed"] == 1
    assert response.json()["cleaning_report"]["rows_before"] == 5
    assert response.json()["cleaning_report"]["rows_after"] == 3

    # TODO 2: GET /datasets/{uploaded_dataset_id}.
    # Assert status 200 and total_rows == 3.
    # Check that the returned records contain student IDs
    # 1, 2, and 5 with scores 80, 90, and 85.
    response = client.get(f"/datasets/{uploaded_dataset_id}")
    assert response.status_code == 200 and response.json()["total_rows"] == 3
    student_ids = []
    scores = []
    for row in response.json()["data"]:
        student_ids.append(row["student_id"])
        scores.append(row["score"])
    assert student_ids == [1, 2, 5]
    assert scores == [80, 90, 85]

def test_retrieve_missing_dataset(client):
    # TODO: Retrieve a dataset ID that does not exist.
    # Assert status 404.
    response = client.get("/datasets/2386983")
    assert response.status_code == 404