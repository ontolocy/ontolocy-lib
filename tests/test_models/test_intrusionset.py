from ontolocy import IntrusionSet


def test_intrusionset():

    adversary = IntrusionSet(
        name="APTX", name_giver="SuperDuper Threat Intel Co.", unique_id="aptx"
    )

    assert adversary.get_primary_property_value() == "aptx"
