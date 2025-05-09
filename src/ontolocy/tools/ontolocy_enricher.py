import hashlib
import json
from abc import abstractmethod
from enum import Enum
from time import sleep
from typing import Optional, Union

import pandas as pd
from neontology import GraphConnection

from ontolocy import CVE, DataOrigin, DomainName, IPAddressNode, OriginGenerated


class SeedTypeEnum(Enum):
    IP = "ip"
    CVE = "cve"
    DOMAIN = "domain"


SEED_MAPPINGS = {
    "ip": {
        "pattern": r"^((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)|((?=.*::)(?!.*::.+::)(::)?([\dA-Fa-f]{1,4}:(:|\b)|){5}|([\dA-Fa-f]{1,4}:){6})((([\dA-Fa-f]{1,4}((?!\3)::|:\b|(?![\dA-Fa-f])))|(?!\2\3)){2}|(((2[0-4]|1\d|[1-9])?\d|25[0-5])\.?\b){4}))$",  # noqa: E501
        "node_type": IPAddressNode,
    },
    "cve": {"pattern": r"^CVE-\d{4}-\d{4,7}$", "node_type": CVE},
    "domain": {
        "pattern": r"^((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}$",
        "node_type": DomainName,
    },
}


def hash_dict(d: dict) -> str:
    return hashlib.sha1(json.dumps(d, sort_keys=True).encode()).hexdigest()


class OntolocyClient:
    retries: int = 3
    cache_queries: bool = True

    def __init__(self):
        super().__init__()
        self.results = {}

        # children must initialise self.parser
        self.parser = None

    def query(self, query, populate=True):
        retries = self.retries

        result = None

        if isinstance(query, dict):
            query_key = hash_dict(query)

        else:
            query_key = query

        if query_key in self.results:
            result = self.results[query_key]

        while retries > 0 and result is None:
            retries = retries - 1

            try:
                result = self._query(query)

                if self.cache_queries:
                    self.results[query_key] = result

                break

            except:  # noqa
                if retries > 0:
                    print(f"Trying again, remaining retries: {retries}")
                    pass
                else:
                    print(f"Failed after {self.retries} retries.")
                    raise

        self.parser.parse_data(result, populate=populate)

    @abstractmethod
    def _query(self, query):
        raise NotImplementedError("Query not implemented")


class OntolocyEnricher:
    seed_type: SeedTypeEnum = None

    def __init__(self):
        super().__init__()

        # children must initialise self.client
        self.client = None

    def get_stale_seeds(self, seeds: list, refresh_days: int) -> list:
        node_class = SEED_MAPPINGS[self.seed_type.value]["node_type"]
        cypher = f"""
        MATCH (n:{node_class.__primarylabel__})<-[r:ORIGIN_GENERATED]-(origin:DataOrigin)
        WHERE origin.name = $data_origin
            AND localdatetime() < r.ontolocy_merged + duration({{days: $days}})
            AND n.{node_class.__primaryproperty__} in $seed_list
        RETURN COLLECT(n.{node_class.__primaryproperty__})
        """

        params = {
            "data_origin": self.__class__.__name__,
            "days": refresh_days,
            "seed_list": seeds,
        }

        gc = GraphConnection()
        recently_enriched = gc.evaluate_query_single(cypher, params)

        if recently_enriched:
            stale = set(seeds) - set(recently_enriched)

        else:
            stale = seeds

        return list(stale)

    def enrich(
        self,
        seeds: Union[str, list],
        populate: bool = True,
        delay: int = 1,
        refresh_days: Optional[int] = None,
    ):
        seeds = list(set(pd.Series(seeds)))

        if refresh_days is not None:
            seeds = self.get_stale_seeds(seeds, refresh_days)

        if len(seeds) == 0:
            print("No stale seeds")
            return

        try:
            query = self._generate_batch_query(seeds)
            self.client.query(query, populate=populate)

        # some clients don't support batch queries
        except NotImplementedError:
            for seed in seeds:
                query = self._generate_single_query(seed)
                self.client.query(query, populate=False)

                if len(seeds) > 1:
                    sleep(delay)

            if populate is True:
                self.client.parser.populate()

        if populate is True:
            data_origin_name = self.__class__.__name__

            data_origin = DataOrigin(
                name=data_origin_name,
            )
            data_origin.merge()

            origin_seed_rels = pd.DataFrame()
            origin_seed_rels["target"] = seeds
            origin_seed_rels["source"] = data_origin.get_pp()

            # because the target type is ambiguous, we need to pass it in explicitly
            OriginGenerated.merge_df(
                origin_seed_rels,
                source_type=DataOrigin,
                target_type=SEED_MAPPINGS[self.seed_type.value]["node_type"],
            )

    def enrich_all(
        self,
        populate: bool = True,
        delay: int = 1,
        refresh_days: Optional[int] = None,
    ):
        all_nodes = SEED_MAPPINGS[self.seed_type.value]["node_type"].match_nodes()

        all_seeds = [x.get_pp() for x in all_nodes]

        self.enrich(
            all_seeds, populate=populate, delay=delay, refresh_days=refresh_days
        )

    @abstractmethod
    def _generate_single_query(self, seed):
        # generate the query
        raise NotImplementedError("Enrichment not implemented")

    @abstractmethod
    def _generate_batch_query(self, seeds):
        # generate the query
        raise NotImplementedError("Enrichment not implemented")
