from ontolocy import IntrusionSet


def test_intrusionset():
    adversary = IntrusionSet(name="APTX", unique_id="aptx")

    assert adversary.get_primary_property_value() == "aptx"
