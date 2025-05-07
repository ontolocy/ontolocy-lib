from click.testing import CliRunner

from ontolocy import (
    IPAddressHasOpenPort,
    ListeningSocketHasBanner,
    ListeningSocketHasJarmHash,
    ListeningSocketHasX509Certificate,
    ListeningSocketUsesPort,
)
from ontolocy.cli import cli
from ontolocy.tools import ShodanIPEnricher, ShodanOntolocyClient, ShodanParser

test_data = {
    "matches": [
        {
            "hash": -709947584,
            "asn": "AS15169",
            "http": {
                "status": 200,
                "robots_hash": None,
                "redirects": [
                    {
                        "host": "www.gslxs12380.gov.cn",
                        "data": 'HTTP/1.1 302 Found\r\nX-Content-Type-Options: nosniff\r\nAccess-Control-Allow-Origin: *\r\nLocation: https://dns.google/\r\nDate: Mon, 05 May 2025 15:44:27 GMT\r\nContent-Type: text/html; charset=UTF-8\r\nServer: HTTP server (unknown)\r\nContent-Length: 216\r\nX-XSS-Protection: 0\r\nX-Frame-Options: SAMEORIGIN\r\nAlt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000\r\n\r\n',
                        "location": "/",
                    }
                ],
                "title_hash": 481067853,
                "securitytxt": None,
                "title": "Google Public DNS",
                "sitemap_hash": None,
                "robots": None,
                "server": "scaffolding on HTTPServer2",
                "dom_hash": -476789325,
                "headers_hash": 2072287827,
                "host": "dns.google",
                "html": '<!DOCTYPE html>\n<html lang="en"> <head> <title>Google Public DNS</title>  <meta charset="UTF-8"> <link href="/static/93dd5954/favicon.png" rel="shortcut icon" type="image/png"> <link href="/static/e6eca759/matter.min.css" rel="stylesheet"> <link href="/static/b8536c37/shared.css" rel="stylesheet"> <meta name="viewport" content="width=device-width, initial-scale=1">  <link href="/static/d05cd6ba/root.css" rel="stylesheet"> </head> <body> <span class="filler top"></span>   <div class="logo" title="Google Public DNS"> <div class="logo-text"><span>Public DNS</span></div> </div>  <form action="/query" method="GET">  <div class="row"> <label class="matter-textfield-outlined"> <input name="name" placeholder="&nbsp;" type="text"> <span>DNS Name</span> <p class="help"> Enter a domain (like example.com) or IP address (like 8.8.8.8 or 2001:4860:4860::8844) here. </p> </label> <button class="matter-button-contained matter-primary" type="submit">Resolve</button> </div> </form>  <span class="filler bottom"></span> <footer class="row"> <a href="https://developers.google.com/speed/public-dns">Help</a> <a href="/cache">Cache Flush</a> <span class="filler"></span> <a href="https://developers.google.com/speed/public-dns/docs/using"> Get Started with Google Public DNS </a> </footer>   <script nonce="34_ccrZ-15Umss2gUuPYkQ">document.forms[0].name.focus();</script> </body> </html>',
                "server_hash": -650751690,
                "location": "/",
                "components": {},
                "securitytxt_hash": None,
                "favicon": {
                    "data": "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAABa1BMVEUAAAA0p100qFM0qFY1pW81\npmg1p141p2M2pHw2pH02pXU3oYs3ook4n5k4oY85np86m6s6m6w7mLo7mLs7mbY7mbc7p1M8lcQ8\nlsM+ks4+ks8+oYo/j9g/j9k/kNg/p1NAiudAi+VAjOFAjeBBh+9BiO1BietChfRChvJEhfRIhvNI\npVJJonNKhPJMhPJMpVJRkcdTh/BXo1FZie5ag+xeie1fhORmlZ5on1Bsnk90juV4m05+jOCAmE2D\ngMuMkdmNk0yQkkuQlNeWltSXj0qliEiubLqvgka0f0W1lbm4m7e7mrS9eUPBdkLHcEDOm5vSZj3S\noJXTZD3UoJLZXTvdWTrgonzhUzjkTjflp3LmSjfoRjboRzbqQzXqRDXqRTXqRjXqRzXsYDHtYjHt\nYzHtqlruqlfveSzveizweyzwr0/yjSbyjib1nSD1nh/1nx/3tSz4rBf4rRb4tyb6uQn6uQr6uhn7\nugj7vAU/At79AAAAAXRSTlMAQObYZgAAArlJREFUeNrt2PVz1EAYxvFlcSnFXQoUXgoUdyvu7ra4\nFy22fz53NJ27Xmx38z7vwpHnl860yXw/c9PJJVGqXuXp9KLGBRG6bHHrWIJ2XeQ8iKB1VIH2Xuw+\nryCkr7dH7vcSRe3PWE9cgqD+xJVETIKgvp5PxCQI68/eyAUI60/uI+IRhPX1MmICBPbnEjEJnC52\nqd9O7+cCuF9p2/8wZS3hAUXHLiZiEnh+zSR/7CE4oPD4SRvYAP7fss1L8AoCA0pOWUjEJQi5y9DL\nB+MC1F4CA8pOIj5A4G1elwNUDfjfAaoGhAGUJAB8Ja4BQX3JL0PO/l8K0P59QQBv31tAJAPQYn2v\n5yIC9D2eDImkAe0EIlTf4fXEPiJkvxSwZTe2XyZIXgUC+yWCefh+oWDmoEBfHXd5FQjsK3V5Ww5g\nqUxfqdtHMvtzhPJKmYfnVqf70/qF+qa5Gwc6+xPWyfRNsgenOwBLZP4BTGtXdrb3ewYkLgFm3O4e\na/XTrwIRAtOxx5c2j12CVxHhBSa9W4dGAQuI8AKTtUdnFzX6s7YSXmBydm2/nrqG8ACTu3unjhLB\nBaZoRHBBYd+caT/08CYAoDCfPvz1navnh3ZwCnzqf2Yb+/Kq6djFAfDNJ4LRfXt//+bFE3uqCAL6\n4whjjusXTh4cYASUnWaz9lOunyOwcn0swOlUIEDJASp8ANkCwQ+gOwCV+pmCbgCoGiAIqNiPDrA1\nIDLAdinACPb/bQDPHRnz/ZgggKkffEdmsQAj1g8EWD6ACngutJx9/ydTa4UA2QTL3S9+O+JThwBa\nisbPr5i+gyDZR1DfGTAM6jsL3sQGPEf1XQVPfqD6roIRWN9R8AnXdxMM4/JugrfIvovgBbTvIHj6\nHZl3EYxg++WEz+B8KeEDPF8ieIfPFxteStSLDM9+ydTzEapelf0GmFdLbOXMqToAAAAASUVORK5C\nYII=\n",
                    "hash": 56641965,
                    "location": "https://dns.google:443/static/93dd5954/favicon.png",
                },
                "sitemap": None,
                "html_hash": -1735016651,
            },
            "os": None,
            "timestamp": "2025-05-05T15:44:28.546745",
            "isp": "Google LLC",
            "transport": "tcp",
            "_shodan": {
                "region": "na",
                "module": "https",
                "ptr": True,
                "options": {
                    "hostname": "www.gslxs12380.gov.cn",
                    "scan": "la91aS48ut0glJwc",
                },
                "id": "fd4a9812-4926-44e2-a3ec-2d4e9341a515",
                "crawler": "85a5be66a1913a867d4f8cd62bd10fb79f410a2a",
            },
            "ssl": {
                "chain_sha256": [
                    "e3ef63ea4488288a7b1a91723282a9a7eb1ed581d798db92d9e22b143d75d99d",
                    "e6fe22bf45e4f0d3b85c59e02c0f495418e1eb8d3210f788d48cd5e1cb547cd4",
                    "3ee0278df71fa3c125c4cd487f01d774694e6fc57e0cd94c24efd769133918e5",
                ],
                "jarm": "29d3fd00029d29d00042d43d00041d598ac0c1012db967bb1ad0ff2491b3ae",
                "tlsext": [
                    {"id": 51, "name": "key_share"},
                    {"id": 43, "name": "supported_versions"},
                ],
                "chain": [
                    "-----BEGIN CERTIFICATE-----\nMIIFsjCCBJqgAwIBAgIRANefuC6K+ovKCfYY8k6W7o4wDQYJKoZIhvcNAQELBQAw\nOzELMAkGA1UEBhMCVVMxHjAcBgNVBAoTFUdvb2dsZSBUcnVzdCBTZXJ2aWNlczEM\nMAoGA1UEAxMDV1IyMB4XDTI1MDMzMTA4NTYyNVoXDTI1MDYyMzA4NTYyNFowFTET\nMBEGA1UEAxMKZG5zLmdvb2dsZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC\nggEBALPmPMEZ1UJUcsPutUkt+9sEby2kVJ/u0O1hmBQv+VUzclRnTvvZyBphpXAm\n+gVQk44T8ws8VsgJWkT59SfGBgScJuFS/VMyERBXj9I78xSq4fSDGqIrbrttw+L3\nsKEU+N+xTKwyp0AuTBVvCOWUW1PCeK/FGwsYZ4gWwfeY+EZJe0WWZInpOHE11NyJ\nTf3eIVJkelVeZ6K8g3YdDu2pEFufGFdD6+8UfKAe7AA21yuNhzRdjDv6Gkyd9PLP\nvBDP4buFldCIUyzQLzZudo8ENtcLmnnauODXdqwND3zagWgFeaZapYC6dIfGsjcE\nr/OYw2tW0ZCRkvXB2IZrjc2lA00CAwEAAaOCAtUwggLRMA4GA1UdDwEB/wQEAwIF\noDATBgNVHSUEDDAKBggrBgEFBQcDATAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBTN\nrdYtfI6BIqMZtSytrpe8FhrZ3zAfBgNVHSMEGDAWgBTeGx7teRXUPjckwyG77DQ5\nbUKyMDBYBggrBgEFBQcBAQRMMEowIQYIKwYBBQUHMAGGFWh0dHA6Ly9vLnBraS5n\nb29nL3dyMjAlBggrBgEFBQcwAoYZaHR0cDovL2kucGtpLmdvb2cvd3IyLmNydDCB\nrAYDVR0RBIGkMIGhggpkbnMuZ29vZ2xlgg5kbnMuZ29vZ2xlLmNvbYIQKi5kbnMu\nZ29vZ2xlLmNvbYILODg4OC5nb29nbGWCEGRuczY0LmRucy5nb29nbGWHBAgICAiH\nBAgIBASHECABSGBIYAAAAAAAAAAAiIiHECABSGBIYAAAAAAAAAAAiESHECABSGBI\nYAAAAAAAAAAAZGSHECABSGBIYAAAAAAAAAAAAGQwEwYDVR0gBAwwCjAIBgZngQwB\nAgEwNgYDVR0fBC8wLTAroCmgJ4YlaHR0cDovL2MucGtpLmdvb2cvd3IyL0dTeVQx\nTjRQQnJnLmNybDCCAQQGCisGAQQB1nkCBAIEgfUEgfIA8AB1AMz7D2qFcQll/pWb\nU87psnwi6YVcDZeNtql+VMD+TA2wAAABleuhirAAAAQDAEYwRAIgFPLROQyXIQq1\n2xULemHhc2URM33skWAKtijXpC5EHJ0CIFvTL7LfSUwVPCBJw411ehyNwHMAVWLj\n6i23QVIOC5uSAHcAzxFW7tUufK/zh1vZaS6b6RpxZ0qwF+ysAdJbd87MOwgAAAGV\n66GKrwAABAMASDBGAiEAqqthdLp3Bsnjn8/emMfoIEWAbR1apX354Rl1XpVv56kC\nIQCKAyXMGeDemyTKmz9eUcNqKf21KKt+bnLtvM2ayXoIxTANBgkqhkiG9w0BAQsF\nAAOCAQEAOr+QeyGp/4nIER7r4kyalVPQgxOUlKbEPuI1luaADPbR8IS/DOZceTT/\nfy0GduIA/wYJHQjWMWczk59XOu3kyK7AhU581nNhkNgNy+wsM/cEIW0zkE4Bde3M\nYYBHc9WlbdkulOoM22vnqA0XbfD//Z5/LZphZD0cFOIbTC1D+CgXc8GqJNGFO50+\nCbshWH4rbEp+nGDwsSfq7SyrS+Xz8s37PblwmkbN0m4vJanSuWmewQOaDLxvM45z\ne6kR2xpglnUmOOMRfrEXDVIS6GD2dbGjfMx2by1JeC6mYaKPxy4zNbS1CvCMEAfT\n0J5RIPOhlhfvFiOV4X9EAublmo+nRw==\n-----END CERTIFICATE-----\n",
                    "-----BEGIN CERTIFICATE-----\nMIIFCzCCAvOgAwIBAgIQf/AFoHxM3tEArZ1mpRB7mDANBgkqhkiG9w0BAQsFADBH\nMQswCQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExM\nQzEUMBIGA1UEAxMLR1RTIFJvb3QgUjEwHhcNMjMxMjEzMDkwMDAwWhcNMjkwMjIw\nMTQwMDAwWjA7MQswCQYDVQQGEwJVUzEeMBwGA1UEChMVR29vZ2xlIFRydXN0IFNl\ncnZpY2VzMQwwCgYDVQQDEwNXUjIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK\nAoIBAQCp/5x/RR5wqFOfytnlDd5GV1d9vI+aWqxG8YSau5HbyfsvAfuSCQAWXqAc\n+MGr+XgvSszYhaLYWTwO0xj7sfUkDSbutltkdnwUxy96zqhMt/TZCPzfhyM1IKji\naeKMTj+xWfpgoh6zySBTGYLKNlNtYE3pAJH8do1cCA8Kwtzxc2vFE24KT3rC8gIc\nLrRjg9ox9i11MLL7q8Ju26nADrn5Z9TDJVd06wW06Y613ijNzHoU5HEDy01hLmFX\nxRmpC5iEGuh5KdmyjS//V2pm4M6rlagplmNwEmceOuHbsCFx13ye/aoXbv4r+zgX\nFNFmp6+atXDMyGOBOozAKql2N87jAgMBAAGjgf4wgfswDgYDVR0PAQH/BAQDAgGG\nMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjASBgNVHRMBAf8ECDAGAQH/\nAgEAMB0GA1UdDgQWBBTeGx7teRXUPjckwyG77DQ5bUKyMDAfBgNVHSMEGDAWgBTk\nrysmcRorSCeFL1JmLO/wiRNxPjA0BggrBgEFBQcBAQQoMCYwJAYIKwYBBQUHMAKG\nGGh0dHA6Ly9pLnBraS5nb29nL3IxLmNydDArBgNVHR8EJDAiMCCgHqAchhpodHRw\nOi8vYy5wa2kuZ29vZy9yL3IxLmNybDATBgNVHSAEDDAKMAgGBmeBDAECATANBgkq\nhkiG9w0BAQsFAAOCAgEARXWL5R87RBOWGqtY8TXJbz3S0DNKhjO6V1FP7sQ02hYS\nTL8Tnw3UVOlIecAwPJQl8hr0ujKUtjNyC4XuCRElNJThb0Lbgpt7fyqaqf9/qdLe\nSiDLs/sDA7j4BwXaWZIvGEaYzq9yviQmsR4ATb0IrZNBRAq7x9UBhb+TV+PfdBJT\nDhEl05vc3ssnbrPCuTNiOcLgNeFbpwkuGcuRKnZc8d/KI4RApW//mkHgte8y0YWu\nryUJ8GLFbsLIbjL9uNrizkqRSvOFVU6xddZIMy9vhNkSXJ/UcZhjJY1pXAprffJB\nvei7j+Qi151lRehMCofa6WBmiA4fx+FOVsV2/7R6V2nyAiIJJkEd2nSi5SnzxJrl\nXdaqev3htytmOPvoKWa676ATL/hzfvDaQBEcXd2Ppvy+275W+DKcH0FBbX62xevG\niza3F4ydzxl6NJ8hk8R+dDXSqv1MbRT1ybB5W0k8878XSOjvmiYTDIfyc9acxVJr\nY/cykHipa+te1pOhv7wYPYtZ9orGBV5SGOJm4NrB3K1aJar0RfzxC3ikr7Dyc6Qw\nqDTBU39CluVIQeuQRgwG3MuSxl7zRERDRilGoKb8uY45JzmxWuKxrfwT/478JuHU\n/oTxUFqOl2stKnn7QGTq8z29W+GgBLCXSBxC9epaHM0myFH/FJlniXJfHeytWt0=\n-----END CERTIFICATE-----\n",
                    "-----BEGIN CERTIFICATE-----\nMIIFYjCCBEqgAwIBAgIQd70NbNs2+RrqIQ/E8FjTDTANBgkqhkiG9w0BAQsFADBX\nMQswCQYDVQQGEwJCRTEZMBcGA1UEChMQR2xvYmFsU2lnbiBudi1zYTEQMA4GA1UE\nCxMHUm9vdCBDQTEbMBkGA1UEAxMSR2xvYmFsU2lnbiBSb290IENBMB4XDTIwMDYx\nOTAwMDA0MloXDTI4MDEyODAwMDA0MlowRzELMAkGA1UEBhMCVVMxIjAgBgNVBAoT\nGUdvb2dsZSBUcnVzdCBTZXJ2aWNlcyBMTEMxFDASBgNVBAMTC0dUUyBSb290IFIx\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAthECix7joXebO9y/lD63\nladAPKH9gvl9MgaCcfb2jH/76Nu8ai6Xl6OMS/kr9rH5zoQdsfnFl97vufKj6bwS\niV6nqlKr+CMny6SxnGPb15l+8Ape62im9MZaRw1NEDPjTrETo8gYbEvs/AmQ351k\nKSUjB6G00j0uYODP0gmHu81I8E3CwnqIiru6z1kZ1q+PsAewnjHxgsHA3y6mbWwZ\nDrXYfiYaRQM9sHmklCitD38m5agI/pboPGiUU+6DOogrFZYJsuB6jC511pzrp1Zk\nj5ZPaK49l8KEj8C8QMALXL32h7M1bKwYUH+E4EzNktMg6TO8UpmvMrUpsyUqtEj5\ncuHKZPfmghCN6J3Cioj6OGaK/GP5Afl4/Xtcd/p2h/rs37EOeZVXtL0m79YB0esW\nCruOC7XFxYpVq9Os6pFLKcwZpDIlTirxZUTQAs6qzkm06p98g7BAe+dDq6dso499\niYH6TKX/1Y7DzkvgtdizjkXPdsDtQCv9Uw+wp9U7DbGKogPeMa3Md+pvez7W35Ei\nEua++tgy/BBjFFFy3l3WFpO9KWgz7zpm7AeKJt8T11dleCfeXkkUAKIAf5qoIbap\nsZWwpbkNFhHax2xIPEDgfg1azVY80ZcFuctL7TlLnMQ/0lUTbiSw1nH69MG6zO0b\n9f6BQdgAmD06yK56mDcYBZUCAwEAAaOCATgwggE0MA4GA1UdDwEB/wQEAwIBhjAP\nBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBTkrysmcRorSCeFL1JmLO/wiRNxPjAf\nBgNVHSMEGDAWgBRge2YaRQ2XyolQL30EzTSo//z9SzBgBggrBgEFBQcBAQRUMFIw\nJQYIKwYBBQUHMAGGGWh0dHA6Ly9vY3NwLnBraS5nb29nL2dzcjEwKQYIKwYBBQUH\nMAKGHWh0dHA6Ly9wa2kuZ29vZy9nc3IxL2dzcjEuY3J0MDIGA1UdHwQrMCkwJ6Al\noCOGIWh0dHA6Ly9jcmwucGtpLmdvb2cvZ3NyMS9nc3IxLmNybDA7BgNVHSAENDAy\nMAgGBmeBDAECATAIBgZngQwBAgIwDQYLKwYBBAHWeQIFAwIwDQYLKwYBBAHWeQIF\nAwMwDQYJKoZIhvcNAQELBQADggEBADSkHrEoo9C0dhemMXoh6dFSPsjbdBZBiLg9\nNR3t5P+T4Vxfq7vqfM/b5A3Ri1fyJm9bvhdGaJQ3b2t6yMAYN/olUazsaL+yyEn9\nWprKASOshIArAoyZl+tJaox118fessmXn1hIVw41oeQa1v1vg4Fv74zPl6/AhSrw\n9U5pCZEt4Wi4wStz6dTZ/CLANx8LZh1J7QJVj2fhMtfTJr9w4z30Z209fOU0iOMy\n+qduBmpvvYuR7hZL6Dupszfnw0Skfths18dG9ZKb59UhvmaSGZRVbNQpsg3BZlvi\nd0lIKO2d1xozclOzgjXPYovJJIultzkMu34qQb9Sz/yilrbCgj8=\n-----END CERTIFICATE-----\n",
                ],
                "versions": [
                    "-TLSv1",
                    "-SSLv2",
                    "-SSLv3",
                    "-TLSv1.1",
                    "TLSv1.2",
                    "TLSv1.3",
                ],
                "acceptable_cas": [],
                "alpn": [],
                "cert": {
                    "sig_alg": "sha256WithRSAEncryption",
                    "issued": "20250331085625Z",
                    "expires": "20250623085624Z",
                    "pubkey": {"bits": 2048, "type": "rsa"},
                    "version": 2,
                    "extensions": [
                        {
                            "critical": True,
                            "data": "\\x03\\x02\\x05\\xa0",
                            "name": "keyUsage",
                        },
                        {
                            "data": "0\\n\\x06\\x08+\\x06\\x01\\x05\\x05\\x07\\x03\\x01",
                            "name": "extendedKeyUsage",
                        },
                        {
                            "critical": True,
                            "data": "0\\x00",
                            "name": "basicConstraints",
                        },
                        {
                            "data": '\\x04\\x14\\xcd\\xad\\xd6-|\\x8e\\x81"\\xa3\\x19\\xb5,\\xad\\xae\\x97\\xbc\\x16\\x1a\\xd9\\xdf',
                            "name": "subjectKeyIdentifier",
                        },
                        {
                            "data": "0\\x16\\x80\\x14\\xde\\x1b\\x1e\\xedy\\x15\\xd4>7$\\xc3!\\xbb\\xec49mB\\xb20",
                            "name": "authorityKeyIdentifier",
                        },
                        {
                            "data": "0J0!\\x06\\x08+\\x06\\x01\\x05\\x05\\x070\\x01\\x86\\x15http://o.pki.goog/wr20%\\x06\\x08+\\x06\\x01\\x05\\x05\\x070\\x02\\x86\\x19http://i.pki.goog/wr2.crt",
                            "name": "authorityInfoAccess",
                        },
                        {
                            "data": "0\\x81\\xa1\\x82\\ndns.google\\x82\\x0edns.google.com\\x82\\x10*.dns.google.com\\x82\\x0b8888.google\\x82\\x10dns64.dns.google\\x87\\x04\\x08\\x08\\x08\\x08\\x87\\x04\\x08\\x08\\x04\\x04\\x87\\x10 \\x01H`H`\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x88\\x88\\x87\\x10 \\x01H`H`\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x88D\\x87\\x10 \\x01H`H`\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00dd\\x87\\x10 \\x01H`H`\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00d",
                            "name": "subjectAltName",
                        },
                        {
                            "data": "0\\n0\\x08\\x06\\x06g\\x81\\x0c\\x01\\x02\\x01",
                            "name": "certificatePolicies",
                        },
                        {
                            "data": "0-0+\\xa0)\\xa0\\'\\x86%http://c.pki.goog/wr2/GSyT1N4PBrg.crl",
                            "name": "crlDistributionPoints",
                        },
                        {
                            "data": '\\x04\\x81\\xf2\\x00\\xf0\\x00u\\x00\\xcc\\xfb\\x0fj\\x85q\\te\\xfe\\x95\\x9bS\\xce\\xe9\\xb2|"\\xe9\\x85\\\\\\r\\x97\\x8d\\xb6\\xa9~T\\xc0\\xfeL\\r\\xb0\\x00\\x00\\x01\\x95\\xeb\\xa1\\x8a\\xb0\\x00\\x00\\x04\\x03\\x00F0D\\x02 \\x14\\xf2\\xd19\\x0c\\x97!\\n\\xb5\\xdb\\x15\\x0bza\\xe1se\\x113}\\xec\\x91`\\n\\xb6(\\xd7\\xa4.D\\x1c\\x9d\\x02 [\\xd3/\\xb2\\xdfIL\\x15< I\\xc3\\x8duz\\x1c\\x8d\\xc0s\\x00Ub\\xe3\\xea-\\xb7AR\\x0e\\x0b\\x9b\\x92\\x00w\\x00\\xcf\\x11V\\xee\\xd5.|\\xaf\\xf3\\x87[\\xd9i.\\x9b\\xe9\\x1aqgJ\\xb0\\x17\\xec\\xac\\x01\\xd2[w\\xce\\xcc;\\x08\\x00\\x00\\x01\\x95\\xeb\\xa1\\x8a\\xaf\\x00\\x00\\x04\\x03\\x00H0F\\x02!\\x00\\xaa\\xabat\\xbaw\\x06\\xc9\\xe3\\x9f\\xcf\\xde\\x98\\xc7\\xe8 E\\x80m\\x1dZ\\xa5}\\xf9\\xe1\\x19u^\\x95o\\xe7\\xa9\\x02!\\x00\\x8a\\x03%\\xcc\\x19\\xe0\\xde\\x9b$\\xca\\x9b?^Q\\xc3j)\\xfd\\xb5(\\xab~nr\\xed\\xbc\\xcd\\x9a\\xc9z\\x08\\xc5',
                            "name": "ct_precert_scts",
                        },
                    ],
                    "fingerprint": {
                        "sha256": "e3ef63ea4488288a7b1a91723282a9a7eb1ed581d798db92d9e22b143d75d99d",
                        "sha1": "4197cb049777c5b5a8e40b892f464928960c7813",
                    },
                    "serial": 286613329945138320776922889641180720782,
                    "issuer": {"C": "US", "CN": "WR2", "O": "Google Trust Services"},
                    "expired": False,
                    "subject": {"CN": "dns.google"},
                },
                "cipher": {
                    "version": "TLSv1.3",
                    "bits": 256,
                    "name": "TLS_AES_256_GCM_SHA384",
                },
                "trust": {"revoked": False, "browser": None},
                "handshake_states": [
                    "before SSL initialization",
                    "SSLv3/TLS write client hello",
                    "SSLv3/TLS read server hello",
                    "TLSv1.3 read encrypted extensions",
                    "SSLv3/TLS read server certificate",
                    "TLSv1.3 read server certificate verify",
                    "SSLv3/TLS read finished",
                    "SSLv3/TLS write change cipher spec",
                    "SSLv3/TLS write finished",
                    "SSL negotiation finished successfully",
                ],
                "ja3s": "66e33336e3e99f75410126f42d44cc81",
                "ocsp": {},
            },
            "hostnames": ["dns.google"],
            "location": {
                "city": "Mountain View",
                "region_code": "CA",
                "area_code": None,
                "longitude": -122.11746,
                "latitude": 38.00881,
                "country_code": "US",
                "country_name": "United States",
            },
            "ip": 134744072,
            "domains": ["dns.google"],
            "org": "Google LLC",
            "data": "HTTP/1.1 200 OK\r\nContent-Security-Policy: object-src 'none';base-uri 'self';script-src 'nonce-34_ccrZ-15Umss2gUuPYkQ' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/honest_dns/1_0;frame-ancestors 'none'\r\nStrict-Transport-Security: max-age=31536000; includeSubDomains; preload\r\nX-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Security-Policy-Report-Only: script-src 'none'; form-action 'none'; frame-src 'none'; report-uri https://csp.withgoogle.com/csp/scaffolding/ntdsgswbsc:55:0\r\nCross-Origin-Opener-Policy-Report-Only: same-origin; report-to=ntdsgswbsc:55:0\r\nReport-To: {\"group\":\"ntdsgswbsc:55:0\",\"max_age\":2592000,\"endpoints\":[{\"url\":\"https://csp.withgoogle.com/csp/report-to/scaffolding/ntdsgswbsc:55:0\"}],}\r\nDate: Mon, 05 May 2025 15:44:28 GMT\r\nServer: scaffolding on HTTPServer2\r\nX-XSS-Protection: 0\r\nX-Frame-Options: SAMEORIGIN\r\nAlt-Svc: h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000\r\nAccept-Ranges: none\r\nVary: Accept-Encoding\r\nTransfer-Encoding: chunked\r\n\r\n",
            "port": 443,
            "ip_str": "8.8.8.8",
        },
        {
            "asn": "AS15169",
            "hash": -553166942,
            "os": None,
            "timestamp": "2025-05-05T06:51:45.698058",
            "isp": "Google LLC",
            "transport": "tcp",
            "_shodan": {
                "region": "na",
                "module": "dns-tcp",
                "ptr": True,
                "options": {
                    "hostname": "www.tri-statecomm.net",
                    "scan": "x1lQBalM6lSGsKop",
                },
                "id": "5080b2df-6a02-470a-9697-452ae5f93dba",
                "crawler": "b81ea4b8a1b38c53a5ff8953966f886fc7f2b90b",
            },
            "hostnames": ["dns.google"],
            "location": {
                "city": "Mountain View",
                "region_code": "CA",
                "area_code": None,
                "longitude": -122.11746,
                "latitude": 38.00881,
                "country_code": "US",
                "country_name": "United States",
            },
            "dns": {
                "software": None,
                "recursive": True,
                "resolver_id": None,
                "resolver_hostname": None,
            },
            "ip": 134744072,
            "domains": ["dns.google"],
            "org": "Google LLC",
            "data": "\nRecursion: enabled",
            "port": 53,
            "ip_str": "8.8.8.8",
        },
    ],
    "total": 2,
}


def test_detect():
    parser = ShodanParser()

    assert parser.detect(test_data) is True


def test_detect_bad():
    parser = ShodanParser()

    assert parser.detect("just some text") is False


def test_node_parse(use_graph):
    parser = ShodanParser()

    parser.parse_data(test_data, populate=False)

    ip_df = parser.node_oriented_dfs["IPAddress"]
    port_df = parser.node_oriented_dfs["Port"]
    socket_df = parser.node_oriented_dfs["ListeningSocket"]
    cert_df = parser.node_oriented_dfs["X509Certificate"]
    jarm_df = parser.node_oriented_dfs["JarmHash"]
    banner_df = parser.node_oriented_dfs["Banner"]

    assert len(ip_df.index) == 1
    assert len(port_df.index) == 2
    assert len(socket_df.index) == 2
    assert len(cert_df.index) == 1
    assert len(jarm_df.index) == 1
    assert len(banner_df.index) == 2


def test_relationship_parse(use_graph):
    parser = ShodanParser()

    parser.parse_data(test_data, populate=False)

    ip_port_df = parser.rel_input_dfs[IPAddressHasOpenPort.__relationshiptype__][
        "src_df"
    ]
    socket_port_df = parser.rel_input_dfs[ListeningSocketUsesPort.__relationshiptype__][
        "src_df"
    ]
    socket_banner_df = parser.rel_input_dfs[
        ListeningSocketHasBanner.__relationshiptype__
    ]["src_df"]
    socket_x509_df = parser.rel_input_dfs[
        ListeningSocketHasX509Certificate.__relationshiptype__
    ]["src_df"]
    socket_jarm_df = parser.rel_input_dfs[
        ListeningSocketHasJarmHash.__relationshiptype__
    ]["src_df"]

    assert len(ip_port_df.index) == 2
    assert len(socket_port_df.index) == 2
    assert len(socket_banner_df.index) == 2
    assert len(socket_x509_df.index) == 1
    assert len(socket_jarm_df.index) == 1


def test_populate(use_graph):
    parser = ShodanParser()

    parser.parse_data(test_data, populate=True)

    cypher = "MATCH (n:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]->(p:ListeningSocket) RETURN COUNT(DISTINCT r)"

    assert use_graph.evaluate_query_single(cypher) == 2


def test_enrich_ip(use_graph, monkeypatch):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(ShodanOntolocyClient, "_query", mockreturn)

    enricher = ShodanIPEnricher()
    enricher.enrich("8.8.8.8")

    cypher = "MATCH (n:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]->(p:ListeningSocket) RETURN COUNT(DISTINCT r)"

    assert use_graph.evaluate_query_single(cypher) == 2

    jarm_cypher = "MATCH (p:ListeningSocket)-[r:LISTENING_SOCKET_HAS_JARM_HASH]->(:JarmHash) RETURN COUNT(DISTINCT r)"

    assert use_graph.evaluate_query_single(jarm_cypher) == 1

    x509_cypher = "MATCH (p:ListeningSocket)-[r:LISTENING_SOCKET_HAS_X509_CERTIFICATE]->(:X509Certificate) RETURN COUNT(DISTINCT r)"

    assert use_graph.evaluate_query_single(x509_cypher) == 1

    banner_cypher = "MATCH (p:ListeningSocket)-[r:LISTENING_SOCKET_HAS_BANNER]->(:Banner) RETURN COUNT(DISTINCT p)"

    assert use_graph.evaluate_query_single(banner_cypher) == 2


def test_cli_enrichment(use_graph, monkeypatch):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(ShodanOntolocyClient, "_query", mockreturn)

    runner = CliRunner()

    result = runner.invoke(cli, ["enrich", "ip", "shodan", "8.8.8.8"])

    assert result.exit_code == 0
    assert "Enriching 8.8.8.8" in result.output

    cypher = "MATCH (n:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]->(p:ListeningSocket) RETURN COUNT(DISTINCT r)"

    rel_count = use_graph.evaluate_query_single(cypher)

    assert rel_count == 2


def test_cli_query(use_graph, monkeypatch):
    def mockreturn(self, query):
        return test_data

    monkeypatch.setattr(ShodanOntolocyClient, "_query", mockreturn)

    runner = CliRunner()

    # note, the query doesn't actually get run!
    result = runner.invoke(cli, ["query", "shodan", "ip:8.8.8.8", "port:53,443"])

    assert result.exit_code == 0
    assert "Running query" in result.output

    cypher = "MATCH (n:IPAddress)-[r:IP_ADDRESS_HAS_OPEN_PORT]->(p:ListeningSocket) RETURN COUNT(DISTINCT r)"

    rel_count = use_graph.evaluate_query_single(cypher)

    assert rel_count == 2
