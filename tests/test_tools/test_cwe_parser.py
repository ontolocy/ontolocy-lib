import pytest

from ontolocy.tools import CWEParser

test_data = {
    "Weakness_Catalog": {
        "@Name": "CWE",
        "@Version": "4.16",
        "@Date": "2024-11-19",
        "@xmlns": "http://cwe.mitre.org/cwe-7",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "@xsi:schemaLocation": "http://cwe.mitre.org/cwe-7 http://cwe.mitre.org/data/xsd/cwe_schema_v7.2.xsd",
        "@xmlns:xhtml": "http://www.w3.org/1999/xhtml",
        "Weaknesses": {
            "Weakness": [
                {
                    "@ID": "1004",
                    "@Name": "Sensitive Cookie Without 'HttpOnly' Flag",
                    "@Abstraction": "Variant",
                    "@Structure": "Simple",
                    "@Status": "Incomplete",
                    "Description": "The product uses a cookie to store sensitive information, but the cookie is not marked with the HttpOnly flag.",
                    "Extended_Description": "The HttpOnly flag directs compatible browsers to prevent client-side script from accessing cookies. Including the HttpOnly flag in the Set-Cookie HTTP response header helps mitigate the risk associated with Cross-Site Scripting (XSS) where an attacker's script code might attempt to read the contents of a cookie and exfiltrate information obtained. When set, browsers that support the flag will not reveal the contents of the cookie to a third party via client-side script executed via XSS.",
                    "Related_Weaknesses": {
                        "Related_Weakness": {
                            "@Nature": "ChildOf",
                            "@CWE_ID": "732",
                            "@View_ID": "1000",
                            "@Ordinal": "Primary",
                        }
                    },
                    "Applicable_Platforms": {
                        "Language": {
                            "@Class": "Not Language-Specific",
                            "@Prevalence": "Undetermined",
                        },
                        "Technology": {
                            "@Class": "Web Based",
                            "@Prevalence": "Undetermined",
                        },
                    },
                    "Background_Details": {
                        "Background_Detail": "An HTTP cookie is a small piece of data attributed to a specific website and stored on the user's computer by the user's web browser. This data can be leveraged for a variety of purposes including saving information entered into form fields, recording user activity, and for authentication purposes. Cookies used to save or record information generated by the user are accessed and modified by script code embedded in a web page. While cookies used for authentication are created by the website's server and sent to the user to be attached to future requests. These authentication cookies are often not meant to be accessed by the web page sent to the user, and are instead just supposed to be attached to future requests to verify authentication details."
                    },
                    "Modes_Of_Introduction": {
                        "Introduction": {"Phase": "Implementation"}
                    },
                    "Likelihood_Of_Exploit": "Medium",
                    "Common_Consequences": {
                        "Consequence": [
                            {
                                "Scope": "Confidentiality",
                                "Impact": "Read Application Data",
                                "Note": "If the HttpOnly flag is not set, then sensitive information stored in the cookie may be exposed to unintended parties.",
                            },
                            {
                                "Scope": "Integrity",
                                "Impact": "Gain Privileges or Assume Identity",
                                "Note": "If the cookie in question is an authentication cookie, then not setting the HttpOnly flag may allow an adversary to steal authentication data (e.g., a session ID) and assume the identity of the user.",
                            },
                        ]
                    },
                    "Detection_Methods": {
                        "Detection_Method": {
                            "@Detection_Method_ID": "DM-14",
                            "Method": "Automated Static Analysis",
                            "Description": 'Automated static analysis, commonly referred to as Static Application Security Testing (SAST), can find some instances of this weakness by analyzing source code (or binary/compiled code) without having to execute it. Typically, this is done by building a model of data flow and control flow, then searching for potentially-vulnerable patterns that connect "sources" (origins of input) with "sinks" (destinations where the data interacts with external components, a lower layer such as the OS, etc.)',
                            "Effectiveness": "High",
                        }
                    },
                    "Potential_Mitigations": {
                        "Mitigation": {
                            "Phase": "Implementation",
                            "Description": "Leverage the HttpOnly flag when setting a sensitive cookie in a response.",
                            "Effectiveness": "High",
                            "Effectiveness_Notes": "While this mitigation is effective for protecting cookies from a browser's own scripting engine, third-party components or plugins may have their own engines that allow access to cookies. Attackers might also be able to use XMLHTTPResponse to read the headers directly and obtain the cookie.",
                        }
                    },
                    "Demonstrative_Examples": {
                        "Demonstrative_Example": {
                            "Intro_Text": "In this example, a cookie is used to store a session ID for a client's interaction with a website. The intention is that the cookie will be sent to the website with each request made by the client.",
                            "Body_Text": [
                                "The snippet of code below establishes a new cookie to hold the sessionID.",
                                "The HttpOnly flag is not set for the cookie. An attacker who can perform XSS could insert malicious script such as:",
                                "When the client loads and executes this script, it makes a request to the attacker-controlled web site. The attacker can then log the request and steal the cookie.",
                                "To mitigate the risk, use the setHttpOnly(true) method.",
                            ],
                            "Example_Code": [
                                {
                                    "@Nature": "Bad",
                                    "@Language": "Java",
                                    "xhtml:div": {
                                        "xhtml:br": [None, None],
                                        "#text": 'String sessionID = generateSessionId();Cookie c = new Cookie("session_id", sessionID);response.addCookie(c);',
                                    },
                                },
                            ],
                        }
                    },
                    "Observed_Examples": {
                        "Observed_Example": [
                            {
                                "Reference": "CVE-2022-24045",
                                "Description": "Web application for a room automation system has client-side Javascript that sets a sensitive cookie without the HTTPOnly security attribute, allowing the cookie to be accessed.",
                                "Link": "https://www.cve.org/CVERecord?id=CVE-2022-24045",
                            },
                            {
                                "Reference": "CVE-2015-4138",
                                "Description": "Appliance for managing encrypted communications does not use HttpOnly flag.",
                                "Link": "https://www.cve.org/CVERecord?id=CVE-2015-4138",
                            },
                        ]
                    },
                    "References": {
                        "Reference": [
                            {"@External_Reference_ID": "REF-2"},
                            {"@External_Reference_ID": "REF-3"},
                            {"@External_Reference_ID": "REF-4"},
                            {"@External_Reference_ID": "REF-5"},
                        ]
                    },
                    "Mapping_Notes": {
                        "Usage": "Allowed",
                        "Rationale": "This CWE entry is at the Variant level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.",
                        "Comments": "Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.",
                        "Reasons": {"Reason": {"@Type": "Acceptable-Use"}},
                    },
                    "Content_History": {
                        "Submission": {
                            "Submission_Name": "CWE Content Team",
                            "Submission_Organization": "MITRE",
                            "Submission_Date": "2017-01-02",
                            "Submission_Version": "2.10",
                            "Submission_ReleaseDate": "2017-01-19",
                        },
                        "Modification": [
                            {
                                "Modification_Name": "CWE Content Team",
                                "Modification_Organization": "MITRE",
                                "Modification_Date": "2017-11-08",
                                "Modification_Comment": "updated Applicable_Platforms, References, Relationships",
                            },
                            {
                                "Modification_Name": "CWE Content Team",
                                "Modification_Organization": "MITRE",
                                "Modification_Date": "2023-10-26",
                                "Modification_Comment": "updated Observed_Examples",
                            },
                        ],
                    },
                },
                {
                    "@ID": "1007",
                    "@Name": "Insufficient Visual Distinction of Homoglyphs Presented to User",
                    "@Abstraction": "Base",
                    "@Structure": "Simple",
                    "@Status": "Incomplete",
                    "Description": "The product displays information or identifiers to a user, but the display mechanism does not make it easy for the user to distinguish between visually similar or identical glyphs (homoglyphs), which may cause the user to misinterpret a glyph and perform an unintended, insecure action.",
                    "Extended_Description": {
                        "xhtml:p": [
                            'Some glyphs, pictures, or icons can be semantically distinct to a program, while appearing very similar or identical to a human user. These are referred to as homoglyphs. For example, the lowercase "l" (ell) and uppercase "I" (eye) have different character codes, but these characters can be displayed in exactly the same way to a user, depending on the font. This can also occur between different character sets. For example, the Latin capital letter "A" and the Greek capital letter "Α" (Alpha) are treated as distinct by programs, but may be displayed in exactly the same way to a user. Accent marks may also cause letters to appear very similar, such as the Latin capital letter grave mark "À" and its equivalent "Á" with the acute accent.',
                            "Adversaries can exploit this visual similarity for attacks such as phishing, e.g. by providing a link to an attacker-controlled hostname that looks like a hostname that the victim trusts. In a different use of homoglyphs, an adversary may create a back door username that is visually similar to the username of a regular user, which then makes it more difficult for a system administrator to detect the malicious username while reviewing logs.",
                        ]
                    },
                    "Related_Weaknesses": {
                        "Related_Weakness": {
                            "@Nature": "ChildOf",
                            "@CWE_ID": "451",
                            "@View_ID": "1000",
                            "@Ordinal": "Primary",
                        }
                    },
                    "Weakness_Ordinalities": {
                        "Weakness_Ordinality": {"Ordinality": "Resultant"}
                    },
                    "Applicable_Platforms": {
                        "Language": {
                            "@Class": "Not Language-Specific",
                            "@Prevalence": "Undetermined",
                        },
                        "Technology": {
                            "@Class": "Web Based",
                            "@Prevalence": "Sometimes",
                        },
                    },
                    "Alternate_Terms": {
                        "Alternate_Term": {
                            "Term": "Homograph Attack",
                            "Description": '"Homograph" is often used as a synonym of "homoglyph" by researchers, but according to Wikipedia, a homograph is a word that has multiple, distinct meanings.',
                        }
                    },
                    "Modes_Of_Introduction": {
                        "Introduction": [
                            {
                                "Phase": "Architecture and Design",
                                "Note": "This weakness may occur when characters from various character sets are allowed to be interchanged within a URL, username, email address, etc. without any notification to the user or underlying system being used.",
                            },
                            {"Phase": "Implementation"},
                        ]
                    },
                    "Likelihood_Of_Exploit": "Medium",
                    "Common_Consequences": {
                        "Consequence": {
                            "Scope": ["Integrity", "Confidentiality"],
                            "Impact": "Other",
                            "Note": "An attacker may ultimately redirect a user to a malicious website, by deceiving the user into believing the URL they are accessing is a trusted domain. However, the attack can also be used to forge log entries by using homoglyphs in usernames. Homoglyph manipulations are often the first step towards executing advanced attacks such as stealing a user's credentials, Cross-Site Scripting (XSS), or log forgery. If an attacker redirects a user to a malicious site, the attacker can mimic a trusted domain to steal account credentials and perform actions on behalf of the user, without the user's knowledge. Similarly, an attacker could create a username for a website that contains homoglyph characters, making it difficult for an admin to review logs and determine which users performed which actions.",
                        }
                    },
                    "Detection_Methods": {
                        "Detection_Method": {
                            "Method": "Manual Dynamic Analysis",
                            "Description": "If utilizing user accounts, attempt to submit a username that contains homoglyphs. Similarly, check to see if links containing homoglyphs can be sent via email, web browsers, or other mechanisms.",
                            "Effectiveness": "Moderate",
                        }
                    },
                    "Potential_Mitigations": {
                        "Mitigation": [
                            {
                                "Phase": "Implementation",
                                "Description": {
                                    "xhtml:p": [
                                        "Use a browser that displays Punycode for IDNs in the URL and status bars, or which color code various scripts in URLs.",
                                        "Due to the prominence of homoglyph attacks, several browsers now help safeguard against this attack via the use of Punycode. For example, Mozilla Firefox and Google Chrome will display IDNs as Punycode if top-level domains do not restrict which characters can be used in domain names or if labels mix scripts for different languages.",
                                    ]
                                },
                            },
                            {
                                "Phase": "Implementation",
                                "Description": {
                                    "xhtml:p": [
                                        "Use an email client that has strict filters and prevents messages that mix character sets to end up in a user's inbox.",
                                        "Certain email clients such as Google's GMail prevent the use of non-Latin characters in email addresses or in links contained within emails. This helps prevent homoglyph attacks by flagging these emails and redirecting them to a user's spam folder.",
                                    ]
                                },
                            },
                        ]
                    },
                    "Demonstrative_Examples": {
                        "Demonstrative_Example": [
                            {
                                "Intro_Text": "The following looks like a simple, trusted URL that a user may frequently access.",
                                "Example_Code": {
                                    "@Nature": "Attack",
                                    "xhtml:div": "http://www.еxаmрlе.соm",
                                },
                                "Body_Text": 'However, the URL above is comprised of Cyrillic characters that look identical to the expected ASCII characters. This results in most users not being able to distinguish between the two and assuming that the above URL is trusted and safe. The "e" is actually the "CYRILLIC SMALL LETTER IE" which is represented in HTML as the character &#x435, while the "a" is actually the "CYRILLIC SMALL LETTER A" which is represented in HTML as the character &#x430.  The "p", "c", and "o" are also Cyrillic characters in this example. Viewing the source reveals a URL of "http://www.&#x435;x&#x430;m&#x440;l&#x435;.&#x441;&#x43e;m". An adversary can utilize this approach to perform an attack such as a phishing attack in order to drive traffic to a malicious website.',
                            },
                            {
                                "Intro_Text": "The following displays an example of how creating usernames containing homoglyphs can lead to log forgery.",
                                "Body_Text": [
                                    "Assume an adversary visits a legitimate, trusted domain and creates an account named \"admin\", except the 'a' and 'i' characters are Cyrillic characters instead of the expected ASCII. Any actions the adversary performs will be saved to the log file and look like they came from a legitimate administrator account.",
                                    'Upon closer inspection, the account that generated three of these log entries is "&#x430;dm&#x456;n". Only the third log entry is by the legitimate admin account. This makes it more difficult to determine which actions were performed by the adversary and which actions were executed by the legitimate "admin" account.',
                                ],
                                "Example_Code": {
                                    "@Nature": "Result",
                                    "xhtml:div": {
                                        "xhtml:br": [None, None, None, None],
                                        "#text": '123.123.123.123 аdmіn [17/Jul/2017:09:05:49 -0400] "GET /example/users/userlist HTTP/1.1" 401 12846\n\t\t  123.123.123.123 аdmіn [17/Jul/2017:09:06:51 -0400] "GET /example/users/userlist HTTP/1.1" 200 4523\n\t\t  123.123.123.123 admin [17/Jul/2017:09:10:02 -0400] "GET /example/users/editusers HTTP/1.1" 200 6291\n\t\t  123.123.123.123 аdmіn [17/Jul/2017:09:10:02 -0400] "GET /example/users/editusers HTTP/1.1" 200 6291',
                                    },
                                },
                            },
                        ]
                    },
                    "Observed_Examples": {
                        "Observed_Example": [
                            {
                                "Reference": "CVE-2013-7236",
                                "Description": "web forum allows impersonation of users with homoglyphs in account names",
                                "Link": "https://www.cve.org/CVERecord?id=CVE-2013-7236",
                            },
                            {
                                "Reference": "CVE-2012-0584",
                                "Description": "Improper character restriction in URLs in web browser",
                                "Link": "https://www.cve.org/CVERecord?id=CVE-2012-0584",
                            },
                        ]
                    },
                    "Related_Attack_Patterns": {
                        "Related_Attack_Pattern": {"@CAPEC_ID": "632"}
                    },
                    "References": {
                        "Reference": [
                            {
                                "@External_Reference_ID": "REF-7",
                                "@Section": 'Chapter 11, "Canonical Representation Issues", Page 382',
                            },
                            {"@External_Reference_ID": "REF-8"},
                        ]
                    },
                    "Mapping_Notes": {
                        "Usage": "Allowed",
                        "Rationale": "This CWE entry is at the Base level of abstraction, which is a preferred level of abstraction for mapping to the root causes of vulnerabilities.",
                        "Comments": "Carefully read both the name and description to ensure that this mapping is an appropriate fit. Do not try to 'force' a mapping to a lower-level Base/Variant simply to comply with this preferred level of abstraction.",
                        "Reasons": {"Reason": {"@Type": "Acceptable-Use"}},
                    },
                    "Content_History": {
                        "Submission": {
                            "Submission_Name": "CWE Content Team",
                            "Submission_Organization": "MITRE",
                            "Submission_Date": "2017-07-24",
                            "Submission_Version": "2.12",
                            "Submission_ReleaseDate": "2017-11-08",
                        },
                        "Modification": [
                            {
                                "Modification_Name": "CWE Content Team",
                                "Modification_Organization": "MITRE",
                                "Modification_Date": "2018-03-27",
                                "Modification_Comment": "updated Demonstrative_Examples, Description, References",
                            },
                            {
                                "Modification_Name": "CWE Content Team",
                                "Modification_Organization": "MITRE",
                                "Modification_Date": "2023-06-29",
                                "Modification_Comment": "updated Mapping_Notes",
                            },
                        ],
                    },
                },
            ]
        },
    }
}


def test_detect():
    parser = CWEParser()

    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = CWEParser()

    assert parser.detect("just some text") is False


def test_node_parse():
    parser = CWEParser()

    parser.parse_data(test_data, populate=False)

    node_df = parser.node_oriented_dfs["CWE"]
    assert len(node_df.index) == 2
    assert node_df["cwe_id"].tolist() == ["1004", "1007"]


def test_populate(use_graph):
    parser = CWEParser()

    parser.parse_data(test_data, populate=True)

    cypher = """MATCH (n:CWE) RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(cypher) == 2


@pytest.mark.slow
@pytest.mark.webtest
def test_populate_web(use_graph):
    parser = CWEParser()

    parser.parse_url("https://cwe.mitre.org/data/xml/cwec_v4.17.xml.zip", populate=True)

    cypher = """MATCH (n:CWE) WHERE n.status <> 'Deprecated' RETURN COUNT(DISTINCT n)"""

    assert use_graph.evaluate_query_single(cypher) == 943
