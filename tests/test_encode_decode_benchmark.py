# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# See COPYING for copyright and distribution information.
#

import time
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from pyndn.util import Blob
from pyndn import Name
from pyndn import Data
from pyndn import KeyLocatorType
from pyndn import Sha256WithRsaSignature
from pyndn.security.identity import MemoryPrivateKeyStorage

def getNowSeconds():
    return time.clock()

# Get a raw string.
DEFAULT_PUBLIC_KEY_DER = "".join(map(chr, bytearray([
0x30, 0x81, 0x9F, 0x30, 0x0D, 0x06, 0x09, 0x2A, 0x86, 0x48, 0x86, 0xF7, 0x0D, 0x01, 0x01, 0x01, 0x05, 0x00, 0x03, 0x81,
0x8D, 0x00, 0x30, 0x81, 0x89, 0x02, 0x81, 0x81, 0x00, 0xE1, 0x7D, 0x30, 0xA7, 0xD8, 0x28, 0xAB, 0x1B, 0x84, 0x0B, 0x17,
0x54, 0x2D, 0xCA, 0xF6, 0x20, 0x7A, 0xFD, 0x22, 0x1E, 0x08, 0x6B, 0x2A, 0x60, 0xD1, 0x6C, 0xB7, 0xF5, 0x44, 0x48, 0xBA,
0x9F, 0x3F, 0x08, 0xBC, 0xD0, 0x99, 0xDB, 0x21, 0xDD, 0x16, 0x2A, 0x77, 0x9E, 0x61, 0xAA, 0x89, 0xEE, 0xE5, 0x54, 0xD3,
0xA4, 0x7D, 0xE2, 0x30, 0xBC, 0x7A, 0xC5, 0x90, 0xD5, 0x24, 0x06, 0x7C, 0x38, 0x98, 0xBB, 0xA6, 0xF5, 0xDC, 0x43, 0x60,
0xB8, 0x45, 0xED, 0xA4, 0x8C, 0xBD, 0x9C, 0xF1, 0x26, 0xA7, 0x23, 0x44, 0x5F, 0x0E, 0x19, 0x52, 0xD7, 0x32, 0x5A, 0x75,
0xFA, 0xF5, 0x56, 0x14, 0x4F, 0x9A, 0x98, 0xAF, 0x71, 0x86, 0xB0, 0x27, 0x86, 0x85, 0xB8, 0xE2, 0xC0, 0x8B, 0xEA, 0x87,
0x17, 0x1B, 0x4D, 0xEE, 0x58, 0x5C, 0x18, 0x28, 0x29, 0x5B, 0x53, 0x95, 0xEB, 0x4A, 0x17, 0x77, 0x9F, 0x02, 0x03, 0x01,
0x00, 0x01  
  ])))

# Get a raw string.
DEFAULT_PRIVATE_KEY_DER = "".join(map(chr, bytearray([
0x30, 0x82, 0x02, 0x5d, 0x02, 0x01, 0x00, 0x02, 0x81, 0x81, 0x00, 0xe1, 0x7d, 0x30, 0xa7, 0xd8, 0x28, 0xab, 0x1b, 0x84,
0x0b, 0x17, 0x54, 0x2d, 0xca, 0xf6, 0x20, 0x7a, 0xfd, 0x22, 0x1e, 0x08, 0x6b, 0x2a, 0x60, 0xd1, 0x6c, 0xb7, 0xf5, 0x44,
0x48, 0xba, 0x9f, 0x3f, 0x08, 0xbc, 0xd0, 0x99, 0xdb, 0x21, 0xdd, 0x16, 0x2a, 0x77, 0x9e, 0x61, 0xaa, 0x89, 0xee, 0xe5,
0x54, 0xd3, 0xa4, 0x7d, 0xe2, 0x30, 0xbc, 0x7a, 0xc5, 0x90, 0xd5, 0x24, 0x06, 0x7c, 0x38, 0x98, 0xbb, 0xa6, 0xf5, 0xdc,
0x43, 0x60, 0xb8, 0x45, 0xed, 0xa4, 0x8c, 0xbd, 0x9c, 0xf1, 0x26, 0xa7, 0x23, 0x44, 0x5f, 0x0e, 0x19, 0x52, 0xd7, 0x32,
0x5a, 0x75, 0xfa, 0xf5, 0x56, 0x14, 0x4f, 0x9a, 0x98, 0xaf, 0x71, 0x86, 0xb0, 0x27, 0x86, 0x85, 0xb8, 0xe2, 0xc0, 0x8b,
0xea, 0x87, 0x17, 0x1b, 0x4d, 0xee, 0x58, 0x5c, 0x18, 0x28, 0x29, 0x5b, 0x53, 0x95, 0xeb, 0x4a, 0x17, 0x77, 0x9f, 0x02,
0x03, 0x01, 0x00, 0x01, 0x02, 0x81, 0x80, 0x1a, 0x4b, 0xfa, 0x4f, 0xa8, 0xc2, 0xdd, 0x69, 0xa1, 0x15, 0x96, 0x0b, 0xe8,
0x27, 0x42, 0x5a, 0xf9, 0x5c, 0xea, 0x0c, 0xac, 0x98, 0xaa, 0xe1, 0x8d, 0xaa, 0xeb, 0x2d, 0x3c, 0x60, 0x6a, 0xfb, 0x45,
0x63, 0xa4, 0x79, 0x83, 0x67, 0xed, 0xe4, 0x15, 0xc0, 0xb0, 0x20, 0x95, 0x6d, 0x49, 0x16, 0xc6, 0x42, 0x05, 0x48, 0xaa,
0xb1, 0xa5, 0x53, 0x65, 0xd2, 0x02, 0x99, 0x08, 0xd1, 0x84, 0xcc, 0xf0, 0xcd, 0xea, 0x61, 0xc9, 0x39, 0x02, 0x3f, 0x87,
0x4a, 0xe5, 0xc4, 0xd2, 0x07, 0x02, 0xe1, 0x9f, 0xa0, 0x06, 0xc2, 0xcc, 0x02, 0xe7, 0xaa, 0x6c, 0x99, 0x8a, 0xf8, 0x49,
0x00, 0xf1, 0xa2, 0x8c, 0x0c, 0x8a, 0xb9, 0x4f, 0x6d, 0x73, 0x3b, 0x2c, 0xb7, 0x9f, 0x8a, 0xa6, 0x7f, 0x9b, 0x9f, 0xb7,
0xa1, 0xcc, 0x74, 0x2e, 0x8f, 0xb8, 0xb0, 0x26, 0x89, 0xd2, 0xe5, 0x66, 0xe8, 0x8e, 0xa1, 0x02, 0x41, 0x00, 0xfc, 0xe7,
0x52, 0xbc, 0x4e, 0x95, 0xb6, 0x1a, 0xb4, 0x62, 0xcc, 0xd8, 0x06, 0xe1, 0xdc, 0x7a, 0xa2, 0xb6, 0x71, 0x01, 0xaa, 0x27,
0xfc, 0x99, 0xe5, 0xf2, 0x54, 0xbb, 0xb2, 0x85, 0xe1, 0x96, 0x54, 0x2d, 0xcb, 0xba, 0x86, 0xfa, 0x80, 0xdf, 0xcf, 0x39,
0xe6, 0x74, 0xcb, 0x22, 0xce, 0x70, 0xaa, 0x10, 0x00, 0x73, 0x1d, 0x45, 0x0a, 0x39, 0x51, 0x84, 0xf5, 0x15, 0x8f, 0x37,
0x76, 0x91, 0x02, 0x41, 0x00, 0xe4, 0x3f, 0xf0, 0xf4, 0xde, 0x79, 0x77, 0x48, 0x9b, 0x9c, 0x28, 0x45, 0x26, 0x57, 0x3c,
0x71, 0x40, 0x28, 0x6a, 0xa1, 0xfe, 0xc3, 0xe5, 0x37, 0xa1, 0x03, 0xf6, 0x2d, 0xbe, 0x80, 0x64, 0x72, 0x69, 0x2e, 0x9b,
0x4d, 0xe3, 0x2e, 0x1b, 0xfe, 0xe7, 0xf9, 0x77, 0x8c, 0x18, 0x53, 0x9f, 0xe2, 0xfe, 0x00, 0xbb, 0x49, 0x20, 0x47, 0xdf,
0x01, 0x61, 0x87, 0xd6, 0xe3, 0x44, 0xb5, 0x03, 0x2f, 0x02, 0x40, 0x54, 0xec, 0x7c, 0xbc, 0xdd, 0x0a, 0xaa, 0xde, 0xe6,
0xc9, 0xf2, 0x8d, 0x6c, 0x2a, 0x35, 0xf6, 0x3c, 0x63, 0x55, 0x29, 0x40, 0xf1, 0x32, 0x82, 0x9f, 0x53, 0xb3, 0x9e, 0x5f,
0xc1, 0x53, 0x52, 0x3e, 0xac, 0x2e, 0x28, 0x51, 0xa1, 0x16, 0xdb, 0x90, 0xe3, 0x99, 0x7e, 0x88, 0xa4, 0x04, 0x7c, 0x92,
0xae, 0xd2, 0xe7, 0xd4, 0xe1, 0x55, 0x20, 0x90, 0x3e, 0x3c, 0x6a, 0x63, 0xf0, 0x34, 0xf1, 0x02, 0x41, 0x00, 0x84, 0x5a,
0x17, 0x6c, 0xc6, 0x3c, 0x84, 0xd0, 0x93, 0x7a, 0xff, 0x56, 0xe9, 0x9e, 0x98, 0x2b, 0xcb, 0x5a, 0x24, 0x4a, 0xff, 0x21,
0xb4, 0x9e, 0x87, 0x3d, 0x76, 0xd8, 0x9b, 0xa8, 0x73, 0x96, 0x6c, 0x2b, 0x5c, 0x5e, 0xd3, 0xa6, 0xff, 0x10, 0xd6, 0x8e,
0xaf, 0xa5, 0x8a, 0xcd, 0xa2, 0xde, 0xcb, 0x0e, 0xbd, 0x8a, 0xef, 0xae, 0xfd, 0x3f, 0x1d, 0xc0, 0xd8, 0xf8, 0x3b, 0xf5,
0x02, 0x7d, 0x02, 0x41, 0x00, 0x8b, 0x26, 0xd3, 0x2c, 0x7d, 0x28, 0x38, 0x92, 0xf1, 0xbf, 0x15, 0x16, 0x39, 0x50, 0xc8,
0x6d, 0x32, 0xec, 0x28, 0xf2, 0x8b, 0xd8, 0x70, 0xc5, 0xed, 0xe1, 0x7b, 0xff, 0x2d, 0x66, 0x8c, 0x86, 0x77, 0x43, 0xeb,
0xb6, 0xf6, 0x50, 0x66, 0xb0, 0x40, 0x24, 0x6a, 0xaf, 0x98, 0x21, 0x45, 0x30, 0x01, 0x59, 0xd0, 0xc3, 0xfc, 0x7b, 0xae,
0x30, 0x18, 0xeb, 0x90, 0xfb, 0x17, 0xd3, 0xce, 0xb5
  ])))

def benchmarkEncodeDataSeconds(nIterations, useComplex, useCrypto):
    """
    Loop to encode a data packet nIterations times.
    
    :param nIterations: The number of iterations.
    :type nIterations: int
    :param useComplex: If true, use a large name, large content and all fields.
      If false, use a small name, small content and only required fields.
    :type useComplex: bool
    :param useCrypto: If true, sign the data packet.  If false, use a blank 
      signature.
    :type useCrypto: bool
    :return: A tuple (duration, encoding) where duration is the number of 
      seconds for all iterations and encoding is the wire encoding.
    :rtype: (float, Blob)
    """
    if useComplex:
        # Use a large name and content.
        name = Name(
          "/ndn/ucla.edu/apps/lwndn-test/numbers.txt/%FD%05%05%E8%0C%CE%1D/%00")
        
        contentString = ""
        count = 1
        contentString += "%d" % count
        count += 1
        while len(contentString) < 1170:
            contentString += " %d" % count
            count += 1
        content = Name.fromEscapedString(contentString)
    else:
        # Use a small name and content.
        name = Name("/test")
        content = Name.fromEscapedString("abc")
    finalBlockId = Name("/%00")[0]
    
    # Initialize the private key storage in case useCrypto is true.
    privateKeyStorage = MemoryPrivateKeyStorage()
    #keyChain = KeyChain(IdentityManager(identityStorage, privateKeyStorage), 
    #                    SelfVerifyPolicyManager(identityStorage))
    keyName = Name("/testname/DSK-123")
    certificateName = keyName.getSubName(0, keyName.size() - 1).append(
      "KEY").append(keyName.get(keyName.size() - 1)).append("ID-CERT").append(
      "0")
    privateKeyStorage.setKeyPairForKeyName(
      keyName, DEFAULT_PUBLIC_KEY_DER, DEFAULT_PRIVATE_KEY_DER)
    
    # Set up signatureBits in case useCrypto is false.
    signatureBits = Blob(bytearray(128))
    emptyBlob = Blob([])

    start = getNowSeconds()
    for i in range(nIterations):
        data = Data(name)
        data.setContent(content)
        if useComplex:
            data.getMetaInfo().setFreshnessPeriod(1000)
            data.getMetaInfo().setFinalBlockID(finalBlockId)

        sha256Signature = data.getSignature()
        keyLocator = sha256Signature.getKeyLocator()
        keyLocator.setType(KeyLocatorType.KEYNAME)
        keyLocator.setKeyName(certificateName)
        if useCrypto:
            # Encode once to get the signed portion.
            sha256Signature.setSignature(emptyBlob)
            unsignedEncoding = data.wireEncode()
            sha256Signature.setSignature(privateKeyStorage.sign
              (unsignedEncoding.toSignedBuffer(), keyName))
        else:
            # Set the signature field, but don't sign.
            sha256Signature.setSignature(signatureBits)

        encoding = data.wireEncode()

    finish = getNowSeconds()
        
    return (finish - start, encoding)

# Depending on the Python version, PyCrypto uses str or bytes.
PyCryptoUsesStr = type(SHA256.new().digest()) is str
def verifyData(data, publicKeyDer):
    # Set the data packet's default wire encoding if it is not already there.
    if data.getDefaultWireEncoding().isNull():
      data.wireEncode()

    if not type(data.getSignature()) is Sha256WithRsaSignature:
      raise RuntimeError("signature is not Sha256WithRsaSignature.")
    signatureInfo = data.getSignature()

    # Get the public key.
    publicKey = RSA.importKey(publicKeyDer)
    # Get the bytes to verify.
    signedPortion = data.getDefaultWireEncoding().toSignedBuffer()
    # Convert the signature bits to a raw string.
    if PyCryptoUsesStr:
        signatureBits = "".join(map(chr, signatureInfo.getSignature().buf()))
    else:
        signatureBits = bytes(signatureInfo.getSignature().buf())
        
    # Hash and verify.
    return PKCS1_v1_5.new(publicKey).verify(SHA256.new(signedPortion), 
                                            signatureBits)

def benchmarkDecodeDataSeconds(nIterations, useCrypto, encoding):
    """
    Loop to decode a data packet nIterations times.
    
    :param nIterations: The number of iterations.
    :type nIterations: int
    :param useCrypto: If true, verify the signature.  If false, don't verify.
    :type useCrypto: bool
    :param encoding: The wire encoding to decode.
    :type encoding: Blob
    """
    start = getNowSeconds()
    for i in range(nIterations):
        data = Data()
        data.wireDecode(encoding)
        
        if useCrypto:
            if not verifyData(data, DEFAULT_PUBLIC_KEY_DER):
                raise RuntimeError("Signature verification: FAILED")

    finish = getNowSeconds()
 
    return finish - start
    
def benchmarkEncodeDecodeData(useComplex, useCrypto):
    """
    Call benchmarkEncodeDataSeconds and benchmarkDecodeDataSeconds with 
    appropriate nInterations.  Print the results to stdout.
    
    :param useComplex: See benchmarkEncodeDataSeconds.
    :type useComplex: bool
    :param useCrypto: See benchmarkEncodeDataSeconds.
    :type useCrypto: bool
    """
    nIterations = 1000 if useCrypto else 20000
    (duration, encoding) = benchmarkEncodeDataSeconds(nIterations, useComplex, 
                                                      useCrypto)
    print("Encode " + ("complex" if useComplex else "simple ") + 
          " data: Crypto? " + ("yes" if useCrypto else "no ") +
          ", Duration sec, Hz: " + repr(duration) + ", " + 
          repr(nIterations / duration))

    nIterations = 5000 if useCrypto else 20000
    duration = benchmarkDecodeDataSeconds(nIterations, useCrypto, encoding)
    print("Decode " + ("complex" if useComplex else "simple ") + 
          " data: Crypto? " + ("yes" if useCrypto else "no ") +
          ", Duration sec, Hz: " + repr(duration) + ", " + 
          repr(nIterations / duration))

def main():
    benchmarkEncodeDecodeData(False, False)
    benchmarkEncodeDecodeData(True, False)
    benchmarkEncodeDecodeData(False, True)
    benchmarkEncodeDecodeData(True, True)

main()
