from ontolocy.models.banner import Banner


def test_banner():

    banner_str = "HTTP/1.1 301 Moved Permanently\r\nDate: Thu, 04 Aug 2022 12:17:32 GMT\r\nServer: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16\r\nLocation: https://45.153.243.142/\r\nContent-Length: 231\r\nContent-Type: text/html; charset=iso-8859-1\r\n\r\n"

    sha1_sum = "076824f4bd74c7a7ce6c8d76aabeacc483b8f7fd"

    banner = Banner(banner=banner_str)

    assert banner.banner == banner_str
    assert banner.sha1 == sha1_sum
