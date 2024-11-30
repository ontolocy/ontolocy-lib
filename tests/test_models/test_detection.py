from ontolocy import Detection


def test_detection():
    detection1 = Detection(
        detection_id="DET-1",
        name="Detection Test 1",
        framework="Test Detection Framework",
        source_tags=["sysmon"],
    )

    assert detection1.source_tags == ["sysmon"]


def test_detection_compare():
    detection1 = Detection(
        detection_id="DET-1",
        name="Detection Test 1",
        framework="Test Control Framework",
    )
    detection2 = Detection(
        detection_id="DET-1",
        name="Detection Test 1",
        framework="Test Control Framework",
    )

    assert detection1.get_pp() == detection2.get_pp()
