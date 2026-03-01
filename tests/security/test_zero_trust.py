import sys
sys.path.append('c:\\Users\\thela\\OneDrive\\Desktop\\personal projets\\multi domain supply chain and finance project\\supplychain-finance-platform\\security\\advanced')
from "zero-trust-architecture" import ZeroTrustEngine

def test_create_zero_trust_engine():
    zt_engine = ZeroTrustEngine()
    assert zt_engine is not None
