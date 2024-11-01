from ontolocy import ControlValidationTest


def test_control_validation_test():
    control_test1 = ControlValidationTest(
        test_id="CON-1",
        name="Control Test 1",
        framework="Test Control Framework",
        platform_tags=["windows"],
    )

    assert control_test1.platform_tags == ["windows"]


def test_control_validation_test_compare():
    control_test1 = ControlValidationTest(
        test_id="CON-1", name="Control Test 1", framework="Test Control Framework"
    )
    control_test2 = ControlValidationTest(
        test_id="CON-1", name="Control Test 1", framework="Test Control Framework"
    )

    assert control_test1.get_pp() == control_test2.get_pp()
