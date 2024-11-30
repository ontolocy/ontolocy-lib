from ontolocy.models.jarmhash import JarmHash


def test_jarm():
    jarm = JarmHash(
        jarm="2ad2ad0002ad2ad00042d42d00000069d641f34fe76acdc05c40262f8815e5"
    )

    assert jarm.jarm == "2ad2ad0002ad2ad00042d42d00000069d641f34fe76acdc05c40262f8815e5"
    assert jarm.tls_extensions_hash == "69d641f34fe76acdc05c40262f8815e5"
    assert jarm.cipher_and_tls_version == "2ad2ad0002ad2ad00042d42d000000"
