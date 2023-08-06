# -*- coding: utf-8 -*-

from .basicanalyzer import BasicAnalyzer


class AuthorityKeyIDAnalyzer(BasicAnalyzer):
    """
    Analyzer for finding certificate updates that are signed by a CA with a specified subject key identifier
    """
    name = "AuthorityKeyIDAnalyzer"

    def __init__(self, actions, authority_key_id):
        """
        Find a CA with a specific authority_key_id
        :param actions:
        :param authority_key_id: Certificate authorityKeyID, string separated by colons
        """
        super().__init__(actions)
        if "keyid" in authority_key_id:
            authority_key_id = authority_key_id.replace("keyid:", "")

        authority_key_id = authority_key_id.replace(r"\n", "")
        self.authority_key_id = authority_key_id

    def match(self, update):
        # TODO chain doesn't work!
        if update.chain is None:
            return False

        # TODO chain doesn't work!
        for cert in update.chain:
            if cert.extensions.basicConstraints == "CA:TRUE" and cert.extensions.subjectKeyIdentifier.lower() == self.authority_key_id.lower():
                return True
        return False
