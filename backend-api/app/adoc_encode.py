from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
import hmac, base64, hashlib, json

class AesUtil(object):
    @classmethod
    def encrypt(cls, plain_text, key):
        # AES256/ECB/PKCS7Padding
        cipher = AES.new(key, AES.MODE_ECB)
        padding_text = pad(plain_text.encode('utf-8'), 16, style='pkcs7')
        cipher_text = cipher.encrypt(padding_text)
        # 结果base64编码
        result = base64.urlsafe_b64encode(cipher_text)
        return result.decode('utf-8')

    @classmethod
    def decrypt(cls, encrypt_text, key):
        # AES256/ECB/PKCS7Padding
        encrypt_text = base64.urlsafe_b64decode(encrypt_text)
        decrypter = AES.new(key, AES.MODE_ECB)
        plain_text = decrypter.decrypt(encrypt_text)
        padding_text = unpad(plain_text, 16, 'pkcs7')
        # 结果base64解码
        result = padding_text.decode('utf-8')
        return result


class RsaUtil(object):
    # RSA加密-使用公钥文件
    @classmethod
    def encrypt_with_file(cls, plain_text, public_key_file):
        with open(public_key_file) as f:
            key = f.read()
            result = cls.encrypt(plain_text, key)
            return result

    # RSA加密-使用公钥字符串
    @classmethod
    def encrypt(cls, plain_text, public_key):
        public_key = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(public_key)
        cipher_text = cipher.encrypt(plain_text.encode("utf-8"))
        # base64编码
        result = base64.urlsafe_b64encode(cipher_text).decode('utf-8')
        return result

    @classmethod
    def decrypt_with_file(cls, encrypt_msg, private_key_file):
        key = None
        with open(private_key_file) as f:
            key = f.read()
        # base64解码
        encrypt_msg = base64.urlsafe_b64decode(encrypt_msg)
        # RSA 解密
        private_key = RSA.importKey(key)
        cipher = PKCS1_v1_5.new(private_key)
        result = cipher.decrypt(encrypt_msg, 0).decode('utf-8')
        return result

    @classmethod
    def decrypt(cls, encrypt_msg, private_key):
        # base64解码
        encrypt_msg = base64.urlsafe_b64decode(encrypt_msg)
        # RSA 解密
        private_key = RSA.importKey(private_key)
        cipher = PKCS1_v1_5.new(private_key)
        result = cipher.decrypt(encrypt_msg, 0).decode('utf-8')
        return result


class SignatureUtil(object):
    @classmethod
    def get_hmac256_signature(cls, data, key):
        # json排序序列化
        pre_string = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
        md5_val = hashlib.md5(json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
        digest = hmac.new(key.encode('utf-8'), pre_string, digestmod=hashlib.sha256).digest()
        # base64编码
        result = base64.urlsafe_b64encode(digest)
        v1 = str(result, 'utf-8')
        return v1
