# -*- coding: utf-8 -*-
from .certstreamobject import CertstreamObject


class Issuer(CertstreamObject):
    """Data class for the LeafCert data structure of certstream"""

    def __init__(self, subject, extensions, not_before, not_after, serial_number, fingerprint, as_der, all_domains):
        """
        Data class for the LeafCert data structure of certstream
        :param subject: Certificate subject
        :param extensions: Certificate extensions
        :param not_before: 'Not before' validity field
        :param not_after: 'Not after' validity field
        :param serial_number: Serial number of the certificate
        :param fingerprint: Certificate fingerprint
        :param as_der: DER representation of the certificate
        :param all_domains: List of all domains contained in this cert
        """
        super().__init__()
        self.subject = subject
        self.extensions = extensions
        self.not_before = not_before
        self.not_after = not_after
        self.serial_number = serial_number
        self.fingerprint = fingerprint
        self.as_der = as_der
        self.all_domains = all_domains
