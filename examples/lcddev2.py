#!/usr/bin/env python

from alphalcd.dlcdi2c import LcdI2C  


print("START") 
lcd = LcdI2C(1, 0x27)
with lcd as f:
  lcd.SETBACKLIGHT = '0'
  lcd.RESET = '1'
  lcd.CLEAR = '1'
  lcd.HOME = '1'
  lcd.SETBACKLIGHT = '1'
  lcd.SETCURSOR = '0'
  lcd.SETBLINK = '0'
print("STOP")


    
