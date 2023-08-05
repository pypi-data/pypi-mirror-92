import os
import ssl

from cryptography import x509
from cryptography.hazmat.backends import default_backend

from EasySelenium.common.utils import get_platform


def get_root_ca_certs(linux_certs_dir_path='/etc/ssl/certs'):
    system, _ = get_platform()
    backend = default_backend()

    if system == system.Windows:
        items = ssl.enum_certificates("root")
        for cert_bytes, encoding, is_trusted in items:
            if encoding == "x509_asn":
                cert = x509.load_der_x509_certificate(cert_bytes, backend)
                yield cert

    elif system == system.Linux:
        certs_file_names = os.listdir(linux_certs_dir_path)
        backend = default_backend()
        for cert_file_name in certs_file_names:
            cert_file_path = os.path.join(linux_certs_dir_path, cert_file_name)
            if not os.path.isfile(cert_file_path):
                continue

            with open(cert_file_path, 'rb') as f:
                cert_pem = f.read()
                cert = x509.load_pem_x509_certificate(cert_pem, backend)
                yield cert
    else:
        raise NotImplemented(f'missing implementation for this operating system="{system.value}"')


def main():
    root_ca_certs = get_root_ca_certs()
    root_ca_certs = list(root_ca_certs)  # you can load it into a list if you are planning multiple iterations

    for root_ca_cert in root_ca_certs:
        print(root_ca_cert.issuer)


if __name__ == '__main__':
    main()
