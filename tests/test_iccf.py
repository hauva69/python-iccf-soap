from iccf_xfcc import ICCFClient

def test_client_init():
    # This just tests if the client can be instantiated and contact the WSDL
    # (Might fail without internet or if ICCF blocks the CI environment)
    client = ICCFClient()
    assert client.client is not None
