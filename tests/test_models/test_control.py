from ontolocy import Control


def test_control():
    control1 = Control(
        control_id="CON-1", name="Control 1", framework="Test Control Framework"
    )
    control2 = Control(
        control_id="CON-1", name="Control 1", framework="Test Control Framework"
    )

    assert control1.get_pp() == control2.get_pp()
