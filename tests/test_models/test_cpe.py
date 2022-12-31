from ontolocy.models.cpe import CPE


def test_cpe():

    cve = CPE(cpe="cpe:2.3:o:microsoft:windows_vista:6.0:sp1:-:-:home_premium:-:x64:-")

    assert (
        cve.get_primary_property_value()
        == "cpe:2.3:o:microsoft:windows_vista:*:*:*:*:*:*:*:*"
    )


def test_cpe_hard():

    cve = CPE(cpe="cpe:2.3:a:badgermeter:moni\:\:tool:*:*:*:*:*:*:*:*")

    assert (
        cve.get_primary_property_value()
        == r"cpe:2.3:a:badgermeter:moni\:\:tool:*:*:*:*:*:*:*:*"
    )


def test_cpe_22():

    cve = CPE(cpe="cpe:/a:cisco:adaptive_security_appliance:9.9.2.80")

    assert (
        cve.get_primary_property_value()
        == "cpe:2.3:a:cisco:adaptive_security_appliance:*:*:*:*:*:*:*:*"
    )


def test_cpe_bad():

    cve = CPE(cpe="cpe:/a:cisco:adaptive_security_appliance:9.9.2.80")

    assert (
        cve.get_primary_property_value()
        == "cpe:2.3:a:cisco:adaptive_security_appliance:*:*:*:*:*:*:*:*"
    )
