from py_cryptotp import Cryptotp

otp = Cryptotp(key='xxxxxxxxxxxxxxxx')

raw_otp, hashed_otp = otp.generate(otp_length=6, otp_duration=2)
print(raw_otp, hashed_otp)

print(otp.validate(raw_otp, hashed_otp))
