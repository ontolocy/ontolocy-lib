from typing import ClassVar, List, Optional

from ..node import OntolocyNode

sectors = {
    "agriculture": {
        "sector_id": "agriculture",
        "name": "Agriculture",
        "keywords": ["agriculture", "farming"],
    },
    "aerospace": {
        "sector_id": "aerospace",
        "name": "Aerospace",
        "keywords": ["aerospace", "airport"],
    },
    "automotive": {
        "sector_id": "automotive",
        "name": "Automotive",
        "keywords": ["automotive"],
    },
    "chemical": {
        "sector_id": "chemical",
        "name": "Chemical",
        "keywords": ["chemical"],
    },
    "commercial": {
        "sector_id": "commercial",
        "name": "Commercial",
        "keywords": ["commercial"],
    },
    "communications": {
        "sector_id": "communications",
        "name": "Communications",
        "keywords": [],
    },
    "construction": {
        "sector_id": "construction",
        "name": "Construction",
        "keywords": ["construction"],
    },
    "defense": {
        "sector_id": "defense",
        "name": "Defense",
        "keywords": ["defense industrial base"],
    },
    "education": {
        "sector_id": "education",
        "name": "Education",
        "keywords": ["education", "schoool", "university", "universities"],
    },
    "energy": {
        "sector_id": "energy",
        "name": "Energy",
        "keywords": ["energy"],
    },
    "entertainment": {
        "sector_id": "entertainment",
        "name": "Entertainment",
        "keywords": ["entertainment"],
    },
    "financial-services": {
        "sector_id": "financial-services",
        "name": "Financial Services",
        "keywords": ["financial services"],
    },
    "emergency-services": {
        "sector_id": "emergency-services",
        "name": "Emergency Services",
        "keywords": ["emergency services", "ambulance"],
    },
    "government-local": {
        "sector_id": "government-local",
        "name": "Local Government",
        "keywords": ["local government"],
    },
    "government-national": {
        "sector_id": "government-national",
        "name": "National Government",
        "keywords": ["national government"],
    },
    "government-public-services": {
        "sector_id": "government-public-services",
        "name": "Public Services",
        "keywords": ["public services"],
    },
    "government-regional": {
        "sector_id": "government-regional",
        "name": "Regional Govenment",
        "keywords": ["government regional"],
    },
    "healthcare": {
        "sector_id": "healthcare",
        "name": "Healthcare",
        "keywords": ["healthcare", "hospital", "care home"],
    },
    "hospitality-leisure": {
        "sector_id": "hospitality-leisure",
        "name": "Leisure and Hospitality",
        "keywords": ["leisure", "hospitality", "restaurant", "cafe"],
    },
    "dams": {
        "sector_id": "dams",
        "name": "Dams",
        "keywords": ["dam"],
    },
    "nuclear": {
        "sector_id": "nuclear",
        "name": "Nuclear",
        "keywords": ["nuclear"],
    },
    "water": {
        "sector_id": "water",
        "name": "Water",
        "keywords": ["water"],
    },
    "insurance": {
        "sector_id": "insurance",
        "name": "Insurance",
        "keywords": ["insurance"],
    },
    "manufacturing": {
        "sector_id": "manufacturing",
        "name": "Manufacturing",
        "keywords": ["manufacturing"],
    },
    "mining": {
        "sector_id": "mining",
        "name": "Mining",
        "keywords": ["mining"],
    },
    "non-profit": {
        "sector_id": "non-profit",
        "name": "Non Profit",
        "keywords": ["non profit", "not for profit", "charity"],
    },
    "pharmaceuticals": {
        "sector_id": "pharmaceuticals",
        "name": "Pharmaceuticals",
        "keywords": ["pharmaceuticals"],
    },
    "retail": {
        "sector_id": "retail",
        "name": "Retail",
        "keywords": ["retail"],
    },
    "technology": {
        "sector_id": "technology",
        "name": "Technology",
        "keywords": ["technology"],
    },
    "telecommunications": {
        "sector_id": "telecommunications",
        "name": "Telecommunications",
        "keywords": ["telecommunications"],
    },
    "transportation": {
        "sector_id": "transportation",
        "name": "Transportation",
        "keywords": ["transportation", "rail"],
    },
    "utilities": {
        "sector_id": "utilities",
        "name": "Utilities",
        "keywords": ["utilities"],
    },
}


class Sector(OntolocyNode):

    __primaryproperty__: ClassVar[str] = "unique_id"
    __primarylabel__: ClassVar[Optional[str]] = "Sector"

    name: str
    unique_id: str
    keywords: Optional[List[str]]
