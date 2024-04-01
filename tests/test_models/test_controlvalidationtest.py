from ontolocy import ControlValidationTest


def test_control_validation_test():
    control_test1 = ControlValidationTest(
        test_id="CON-1", name="Control Test 1", framework="Test Control Framework"
    )
    control_test2 = ControlValidationTest(
        test_id="CON-1", name="Control Test 1", framework="Test Control Framework"
    )

    assert (
        control_test1.get_primary_property_value()
        == control_test2.get_primary_property_value()
    )
