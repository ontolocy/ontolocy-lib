from ontolocy import ActorType
from ontolocy.models.actortype import actor_type_taxonomy, ActorTypeEnum


def test_define_actortype():
    actor_type = ActorType(unique_id="nation-state")

    assert actor_type.name == "Nation State"


def test_taxonomy():
    for e in ActorTypeEnum:
        assert e.value in actor_type_taxonomy
