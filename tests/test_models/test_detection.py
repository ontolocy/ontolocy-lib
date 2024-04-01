from ontolocy import Detection


def test_detection():
    detection1 = Detection(
        detection_id="CON-1", name="Control Test 1", framework="Test Control Framework"
    )
    detection2 = Detection(
        detection_id="CON-1", name="Control Test 1", framework="Test Control Framework"
    )

    assert (
        detection1.get_primary_property_value()
        == detection2.get_primary_property_value()
    )
