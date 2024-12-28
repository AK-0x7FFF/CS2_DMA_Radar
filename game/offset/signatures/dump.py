from game.offset.signatures.client import dump_client_signatures
from game.offset.signatures.engine2 import dump_engine2_signatures
from game.offset.signatures.type_hint import SignaturesTypeHint, SignaturesClientTypeHint, SignaturesEngine2TypeHint


def dump_signatures() -> SignaturesTypeHint:
    client_signatures: SignaturesClientTypeHint   = dump_client_signatures().build()
    engine2_signatures: SignaturesEngine2TypeHint = dump_engine2_signatures().build()

    return type("Signatures", (SignaturesTypeHint, ), dict(
        client=client_signatures,
        engine2=engine2_signatures
    ))()


