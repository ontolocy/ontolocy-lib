from ontolocy import UserAccount


def test_control():
    user1 = UserAccount(username="Admin", namespace="TestNamespace")

    user2 = UserAccount(username="Admin", namespace="TestNamespace")

    user3 = UserAccount(username="Admin", local_hostname="MyPC")

    assert user1.get_pp() == user2.get_pp()

    assert user1.get_pp() != user3.get_pp()

    assert str(user1) == "Admin"
