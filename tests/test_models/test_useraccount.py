from ontolocy import UserAccount


def test_control():
    user1 = UserAccount(username="Admin", namespace="TestNamespace")

    user2 = UserAccount(username="Admin", namespace="TestNamespace")

    user3 = UserAccount(username="Admin", local_hostname="MyPC")

    assert user1.get_primary_property_value() == user2.get_primary_property_value()

    assert user1.get_primary_property_value() != user3.get_primary_property_value()

    assert user1.get_identifier() == "Admin"
