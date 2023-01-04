from flipdotapi import remote_sign as sign
import time

sign_url =  "http://192.168.120.61:8080/api/dots"
sign_columns = 96
sign_rows= 16
sign_sim = True
display_font = "0-4-b-3-0"

sign = sign(sign_url, sign_columns, sign_rows, simulator=sign_sim)
# print(sign)
new_time = time.strftime('%I:%M')
# print(new_time)
# new_time = ""
sign.write_text(new_time, alignment="centre", font_name=display_font, fit=True, scroll=False)

sign.clear()
sign.write_text("yeaaaa", alignment="centre", font_name=display_font, fit=False, scroll=False)