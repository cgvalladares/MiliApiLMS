from MiliApiLMS.fingerprint.tools import toolsFingerprint

def test_ListaHuellas_not_none():
    huella=toolsFingerprint.ListaHuellas()
    assert huella!=None


def test_ListaHuellas_has_elements():
    huella=toolsFingerprint.ListaHuellas()
    assert len(huella)>0    
    
def test_ListaHuellas_check_elements_length():
    huella=toolsFingerprint.ListaHuellas()
    for h in huella:
        assert len(h)>0
