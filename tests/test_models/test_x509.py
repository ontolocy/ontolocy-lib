from ontolocy.models.x509certificate import X509Certificate


def testcert():

    cert = X509Certificate(
        sha1="60c0ed8ce1cb4735b4a7fd2f1953363810ba2b7e",
        serial_number="14652236150452427033",
        issuer_cn="DE",
    )

    assert cert.issuer_cn == "DE"
    assert cert.serial_number == "14652236150452427033"
    assert cert.get_pp() == "60c0ed8ce1cb4735b4a7fd2f1953363810ba2b7e"
