"""
Pytest configuration and fixtures for IntelliSearch V2 tests
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Provide test defaults so backend settings can initialize during collection.
os.environ.setdefault('GITHUB_TOKEN_A', 'test-token-a')
os.environ.setdefault('GITHUB_TOKEN_B', 'test-token-b')
os.environ.setdefault('CLIENT_KEY', 'test-key')

# Set pytest asyncio mode
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def valid_client_key():
    """Get valid client key from environment"""
    return os.environ.get('CLIENT_KEY', 'test-key')


@pytest.fixture
def sample_pdf_bytes():
    """Create minimal valid PDF bytes for testing"""
    # Minimal PDF structure
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< >>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF Content) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000203 00000 n 
trailer
<< /Size 5 /Root 1 0 R >>
startxref
299
%%EOF
"""
    return pdf_content


@pytest.fixture
def sample_png_bytes():
    """Create minimal valid PNG bytes for testing"""
    # Minimal 1x1 white PNG
    import struct
    import zlib
    
    # PNG signature
    png_sig = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (1x1, 8-bit grayscale)
    ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 0, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    ihdr = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
    
    # IDAT chunk (white pixel data)
    idat_data = zlib.compress(b'\x00\xff')
    idat_crc = zlib.crc32(b'IDAT' + idat_data) & 0xffffffff
    idat = struct.pack('>I', len(idat_data)) + b'IDAT' + idat_data + struct.pack('>I', idat_crc)
    
    # IEND chunk
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
    
    return png_sig + ihdr + idat + iend
