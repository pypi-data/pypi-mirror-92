import random
from datetime import datetime, timedelta
import hmac
import hashlib


class Cryptotp:

    key: bytes
    identifier: str

    def __init__(self, key: str, ):
        '''
        Parameters:
            key: The secret key which will be used to hash data. Keep it safe
        '''

        self.key = bytes(key, 'utf-8')
        self.identifier = str(random.random())

    def generate(self, otp_length: int, otp_duration: int):
        """
        returns a raw_otp with given length and and a hashed_otp with given expiration time

        Parameters:
            otp_length: length of the OTP which will generated
            otp_duration: minutes the OTP will be valid
        """

        # generating otp by calling random_generator method
        raw_otp = self.__otp_generator(otp_length)

        # converting raw_otp and expiration timestamp into a string separeted by '?'
        expiration_time = int(
            (datetime.now() + timedelta(minutes=otp_duration)).timestamp())

        otp_w_signatures = str(raw_otp) + "?" + \
            str(expiration_time) + self.identifier

        # hasing the string
        hashed_otp = self.__hash_generator(
            otp_w_signatures) + '.' + str(expiration_time)

        # returning generated otp and hashed otp
        return raw_otp, hashed_otp

    def validate(self, user_given_otp, hashed_otp):
        """
        Verifies OTP and returns Boolean value

        Parameters:
            user_given_otp: OTP entered by user
            hashed_otp: The hashed otp previously sent to the client
        """

        # destructuring the hashed_otp
        hashed_otp_object = hashed_otp.split('.')
        hashed_otp = hashed_otp_object[0]
        expiration_time = int(hashed_otp_object[1])

        # checking if the expiration time is in future
        if expiration_time < int(datetime.now().timestamp()):
            return False

        # hashing user_give_otp and validating
        user_given_otp_w_signatures = str(user_given_otp) + "?" + \
            str(expiration_time) + self.identifier

        hashed_user_given_otp = self.__hash_generator(
            user_given_otp_w_signatures)

        if hashed_user_given_otp == hashed_otp:
            return True

        return False

    # random n digit number genetor
    def __otp_generator(self, length):
        start_range = 10**(length - 1)
        end_range = (10**length) - 1

        return random.randint(start_range, end_range)

    # SHA256 hash generator
    def __hash_generator(self, data_string):
        hash = hmac.new(self.key, data_string.encode(
        ), digestmod=hashlib.sha256).hexdigest()

        return hash
