'''
Tests for iccf_xffc.
'''

from iccf_xfcc import ICCFClient # pylint: disable=import-error

def test_client_init():
    '''Test the initialization.'''
    # This just tests if the client can be instantiated and contact the WSDL
    # (Might fail without internet or if ICCF blocks the CI environment)
    client = ICCFClient()
    assert client.client is not None
