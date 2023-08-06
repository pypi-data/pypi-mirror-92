#ValuesConverter V1

#ConverterPrograms
#SpeedConverter
def SpeedConverterProgram():
    #SpeedController
    #Intrudoction
    FloatSpeed = input('Choose what you want to get the value from(m/s,km/h,mi/h):')
    a = float(input('Entered value:'))
    AnswerSpeed = input('Selest the value you want to convert(m/s,km/h,mi/h):')
    #km/h
    if FloatSpeed =='km/h' and AnswerSpeed == 'm/s':
        c = a * 0.28
        print('Answer: '+ str(c) + 'm/s')
    elif FloatSpeed =='km/h' and AnswerSpeed == 'mi/h':
        c = a * 0.6
        print('Answer: '+ str(c) + 'mi/h')
    #m/s
    if FloatSpeed =='m/s' and AnswerSpeed == 'km/h':
        c = a * 3.6
        print('Answer: '+ str(c) + 'km/h')
    elif FloatSpeed =='m/s' and AnswerSpeed == 'mi/h':
        c = a * 2.24
        print('Answer: '+ str(c) + 'mi/h')
    #mi/h
    if FloatSpeed =='mi/h' and AnswerSpeed == 'km/h':
        c = a * 1.6
        print('Answer: '+ str(c) + 'km/h')
    elif FloatSpeed =='mi/h' and AnswerSpeed == 'm/s':
        c = a * 0.45
        print('Answer: '+ str(c) + 'm/s')
    #Error Values
    if (FloatSpeed == 'm/s' and AnswerSpeed == 'm/s') or (FloatSpeed == 'km/h' and AnswerSpeed == 'km/h') or (FloatSpeed == 'mi/h' and AnswerSpeed == 'mi/h'):
        print("You have selected incorrect values. For example, you can't convert km/h to km / h.")

#TimeConverter
def TimeConverterProgram():
    #TimeController
    #Introduction
    FloatTime = input("Choose what you want to get the value from(sec,min,hours(h),day's(d).)")
    a = float(input('Entered value:'))
    AnswerTime = input("Selest the value you want to convert(sec,min,hours(h),day's(d).)")
    #sec
    if FloatTime == 'sec' and AnswerTime == 'min':
        c = a * 0.16
        print('Answer: ' + str(c) + ' min.')
    elif FloatTime == 'sec' and AnswerTime == 'h':
        c = a * 0.00027
        print('Answer: ' + str(c) + ' h.')
    elif FloatTime == 'sec' and AnswerTime == 'd':
        c = a * 0.000011
        print('Answer: ' + str(c) + ' d.')
    #min
    if FloatTime == 'min' and AnswerTime == 'sec':
        c = a * 60
        print('Answer: ' + str(c) + ' sec.')
    elif FloatTime == 'min' and AnswerTime == 'h':
        c = a * 0.01
        print('Answer: ' + str(c) + ' h.')
    elif FloatTime == 'min' and AnswerTime == 'd':
        c = a * 0.00069
        print('Answer: ' + str(c) + ' d.')
    #hours
    if FloatTime == 'h' and AnswerTime == 'sec':
        c = a * 3600
        print('Answer: ' + str(c) + ' sec.')
    elif FloatTime == 'h' and AnswerTime == 'min':
        c = a * 60
        print('Answer: ' + str(c) + ' min.')
    elif FloatTime == 'h' and AnswerTime == 'd':
        c = a * 0.0416
        print('Answer: ' + str(c) + ' d.')
    #day's
    if FloatTime == 'd' and AnswerTime == 'sec':
        c = a * 86400
        print('Answer: ' + str(c) + ' sec.')
    elif FloatTime == 'd' and AnswerTime == 'min':
        c = a * 1440
        print('Answer: ' + str(c) + ' min.')
    elif FloatTime == 'd' and AnswerTime == 'h':
        c = a * 24
        print('Answer: ' + str(c) + ' h.')
    #Error Values
    if (FloatTime == 'sec' and AnswerTime == 'sec') or (FloatTime == 'min' and AnswerTime == 'min') or (FloatTime == 'h' and AnswerTime == 'h') or (FloatTime == 'd' and AnswerTime == 'd'):
        print("You have selected incorrect values. For example, you can't convert sec to sec.")

#WeightConverter
def WeightConverterProgram():
    #WeightController
    #Introduction
    FloatWeight = input("Choose what you want to get the value from(gr,kg,ton(t).)")
    a = float(input('Entered value:'))
    AnswerWeight = input("Selest the value you want to convert(gr,kg,ton(t).)")
    #gr
    if FloatWeight == 'gr' and AnswerWeight == 'kg':
        c = a * 0.001
        print('Answer: ' + str(c) + 'kg.')
    elif FloatWeight == 'gr' and AnswerWeight == 't':
        c = a * 0.000001
        print('Answer: ' + str(c) + 't.')
    #kg
    if FloatWeight == 'kg' and AnswerWeight == 'gr':
        c = a * 1000
        print('Answer: ' + str(c) + 'gr.')
    elif FloatWeight == 'kg' and AnswerWeight == 't':
        c = a * 0.001
        print('Answer: ' + str(c) + 't.')
    #t
    if FloatWeight == 't' and AnswerWeight == 'gr':
        c = a * 1000000
        print('Answer: ' + str(c) + 'gr.')
    elif FloatWeight == 't' and AnswerWeight == 't':
        c = a * 1000
        print('Answer: ' + str(c) + 't.')
    #Error Values.
    if (FloatWeight == 'gr' and AnswerWeight == 'gr') or (FloatWeight == 'kg' and AnswerWeight == 'kg') or (FloatWeight == 't' and AnswerWeight == 't'):
        print("You have selected incorrect values. For example, you can't convert gr to gr.")

#lengthConverter  
def LengthConverterProgram():
    #LengthController
    #Introduction
    FloatLength = input("Choose what you want to get the value from(mm,cm,in,in,de,m,km.)")
    a = float(input('Entered value:'))
    AnswerLenght = input("Selest the value you want to convert(mm,cm,in,de,m,km.)")
    #mm
    if FloatLength == 'mm' and AnswerLenght == 'cm':
        c = a * 0.1
        print('Answer: ' + str(c) + 'cm.')
    elif FloatLength == 'mm' and AnswerLenght == 'in':
        c = a * 0.039
        print('Answer: ' + str(c) + 'in.')
    elif FloatLength == 'mm' and AnswerLenght == 'de':
        c = a * 0.01
        print('Answer: ' + str(c) + 'de.')
    elif FloatLength == 'mm' and AnswerLenght == 'm':
        c = a * 0.001
        print('Answer: ' + str(c) + 'm.')
    elif FloatLength == 'mm' and AnswerLenght == 'km':
        c = a * 0.000001
        print('Answer: ' + str(c) + 'km.')
    #cm
    if FloatLength == 'cm' and AnswerLenght == 'mm':
        c = a * 10
        print('Answer: ' + str(c) + 'mm.')
    elif FloatLength == 'cm' and AnswerLenght == 'in':
        c = a * 0.39
        print('Answer: ' + str(c) + 'in.')
    elif FloatLength == 'cm' and AnswerLenght == 'de':
        c = a * 0.1
        print('Answer: ' + str(c) + 'de.')
    elif FloatLength == 'cm' and AnswerLenght == 'm':
        c = a * 0.01
        print('Answer: ' + str(c) + 'm.')
    elif FloatLength == 'cm' and AnswerLenght == 'km':
        c = a * 0.00001
        print('Answer: ' + str(c) + 'km.')
    #in
    if FloatLength == 'in' and AnswerLenght == 'cm':
        c = a * 2.54
        print('Answer: ' + str(c) + 'cm.')
    elif FloatLength == 'in' and AnswerLenght == 'mm':
        c = a * 25.4
        print('Answer: ' + str(c) + 'mm.')
    elif FloatLength == 'in' and AnswerLenght == 'de':
        c = a * 0.254
        print('Answer: ' + str(c) + 'de.')
    elif FloatLength == 'in' and AnswerLenght == 'm':
        c = a * 0.0254
        print('Answer: ' + str(c) + 'm.')
    elif FloatLength == 'in' and AnswerLenght == 'km':
        c = a * 0.0000254
        print('Answer: ' + str(c) + 'km.')
    #de
    if FloatLength == 'de' and AnswerLenght == 'cm':
        c = a * 10
        print('Answer: ' + str(c) + 'cm.')
    elif FloatLength == 'de' and AnswerLenght == 'mm':
        c = a * 100
        print('Answer: ' + str(c) + 'mm.')
    elif FloatLength == 'de' and AnswerLenght == 'in':
        c = a * 3.937
        print('Answer: ' + str(c) + 'in.')
    elif FloatLength == 'de' and AnswerLenght == 'm':
        c = a * 0.1
        print('Answer: ' + str(c) + 'm.')
    elif FloatLength == 'de' and AnswerLenght == 'km':
        c = a * 0.0001
        print('Answer: ' + str(c) + 'km.')
    #m
    if FloatLength == 'm' and AnswerLenght == 'cm':
        c = a * 100
        print('Answer: ' + str(c) + 'cm.')
    elif FloatLength == 'm' and AnswerLenght == 'mm':
        c = a * 1000
        print('Answer: ' + str(c) + 'mm.')
    elif FloatLength == 'm' and AnswerLenght == 'de':
        c = a * 10
        print('Answer: ' + str(c) + 'de.')
    elif FloatLength == 'm' and AnswerLenght == 'in':
        c = a * 39.37
        print('Answer: ' + str(c) + 'in.')
    elif FloatLength == 'm' and AnswerLenght == 'km':
        c = a * 0.001
        print('Answer: ' + str(c) + 'km.')
    #km
    if FloatLength == 'km' and AnswerLenght == 'cm':
        c = a * 100000
        print('Answer: ' + str(c) + 'cm.')
    elif FloatLength == 'km' and AnswerLenght == 'mm':
        c = a * 1000000
        print('Answer: ' + str(c) + 'mm.')
    elif FloatLength == 'km' and AnswerLenght == 'de':
        c = a * 10000
        print('Answer: ' + str(c) + 'de.')
    elif FloatLength == 'km' and AnswerLenght == 'm':
        c = a * 1000
        print('Answer: ' + str(c) + 'm.')
    elif FloatLength == 'km' and AnswerLenght == 'in':
        c = a * 39370
        print('Answer: ' + str(c) + 'in.')
    #Error Length
    if (FloatLength == 'mm' and AnswerLenght == 'mm') or (FloatLength == 'cm' and AnswerLenght == 'cm') or (FloatLength == 'de' and AnswerLenght == 'de') or (FloatLength == 'in' and AnswerLenght == 'in') or (FloatLength == 'm' and AnswerLenght == 'm') or (FloatLength == 'km' and AnswerLenght == 'km'):
        print("You have selected incorrect values. For example, you can't convert mm to mm.")

#TemperatureConverter
def TemperatureConverterProgram():
    #TemperatureController
    #Intrudoction
    FloatTemp = input('Choose what you want to get the value from(Cels(c),Fahr(f),Kelv(k)):')
    a = float(input('Entered value:'))
    AnswerTemp = input('Selest the value you want to convert(Cels(c),Fahr(f),Kelv(k)):')
    #Celsius
    if FloatTemp =='c' and AnswerTemp == 'f':
        c = (a*1.8+32)
        print('Answer: '+ str(c) + 'f')
    elif FloatTemp =='c' and AnswerTemp == 'k':
        c = (a+273.15)
        print('Answer: '+ str(c) + 'k')
    #Fahrenheit
    if FloatTemp =='f' and AnswerTemp == 'c':
        c = ((a-32)/1.8)
        print('Answer: '+ str(c) + 'c')
    elif FloatTemp =='f' and AnswerTemp == 'k':
        c = ((a+459.67)/1.8)
        print('Answer: '+ str(c) + 'k')
    #Kelvin
    if FloatTemp =='k' and AnswerTemp == 'c':
        c = (a-273.15)
        print('Answer: '+ str(c) + 'c')
    elif FloatTemp =='k' and AnswerTemp == 'f':
        c = (a*1.8-459.67) 
        print('Answer: '+ str(c) + 'f')
    #Error Values
    if (FloatTemp == 'f' and AnswerTemp == 'f') or (FloatTemp == 'c' and AnswerTemp == 'c') or (FloatTemp == 'k' and AnswerTemp == 'k'):
        print("You have selected incorrect values. For example, you can't convert c to c.")

#AreaConverter
def AreaConverterProgram():
    #AreaController
    #Introduction
    FloatArea = input("Choose what you want to get the value from(mm^2,cm^2,de^2,m^2,ap^2,ha^2,km^2):")
    a = float(input('Entered value:'))
    AnswerArea = input("Selest the value you want to convert(mm^2,cm^2,de^2,m^2,ap^2,ha^2,km^2):")
    #mm^2
    if FloatArea == 'mm^2' and AnswerArea == 'cm^2':
        c = a*0.01
        print('Answer: '+ str(c)+'cm^2')
    elif FloatArea == 'mm^2' and AnswerArea == 'de^2':
        c = a*0.0001
        print('Answer: '+ str(c)+'de^2')
    elif FloatArea == 'mm^2' and AnswerArea == 'm^2':
        c = a*0.000001
        print('Answer: '+ str(c)+'m^2')
    elif FloatArea == 'mm^2' and AnswerArea == 'ap^2':
        c = a*0.00000001
        print('Answer: '+ str(c)+'ap^2')
    elif FloatArea == 'mm^2' and AnswerArea == 'ha^2':
        c = a*0.0000000001
        print('Answer: '+ str(c)+'ha^2')
    elif FloatArea == 'mm^2' and AnswerArea == 'km^2':
        c = a*0.000000000001
        print('Answer: '+ str(c)+'km^2')
    #cm^2
    if FloatArea == 'cm^2' and AnswerArea == 'mm^2':
        c = a*100
        print('Answer: '+ str(c)+'mm^2')
    elif FloatArea == 'cm^2' and AnswerArea == 'de^2':
        c = a*0.01
        print('Answer: '+ str(c)+'de^2')
    elif FloatArea == 'cm^2' and AnswerArea == 'm^2':
        c = a*0.0001
        print('Answer: '+ str(c)+'m^2')
    elif FloatArea == 'cm^2' and AnswerArea == 'ap^2':
        c = a*0.000001
        print('Answer: '+ str(c)+'ap^2')
    elif FloatArea == 'cm^2' and AnswerArea == 'ha^2':
        c = a*0.00000001
        print('Answer: '+ str(c)+'ha^2')
    elif FloatArea == 'cm^2' and AnswerArea == 'km^2':
        c = a*0.0000000001
        print('Answer: '+ str(c)+'km^2')
    #de^2
    if FloatArea == 'de^2' and AnswerArea == 'mm^2':
        c = a*10000
        print('Answer: '+ str(c)+'mm^2')
    elif FloatArea == 'de^2' and AnswerArea == 'cm^2':
        c = a*100
        print('Answer: '+ str(c)+'cm^2')
    elif FloatArea == 'de^2' and AnswerArea == 'm^2':
        c = a*0.01
        print('Answer: '+ str(c)+'m^2')
    elif FloatArea == 'de^2' and AnswerArea == 'ap^2':
        c = a*0.0001
        print('Answer: '+ str(c)+'ap^2')
    elif FloatArea == 'de^2' and AnswerArea == 'ha^2':
        c = a*0.000001
        print('Answer: '+ str(c)+'ha^2')
    elif FloatArea == 'de^2' and AnswerArea == 'km^2':
        c = a*0.00000001
        print('Answer: '+ str(c)+'km^2')
    #m^2
    if FloatArea == 'm^2' and AnswerArea == 'mm^2':
        c = a*1000000
        print('Answer: '+ str(c)+'mm^2')
    elif FloatArea == 'm^2' and AnswerArea == 'cm^2':
        c = a*10000
        print('Answer: '+ str(c)+'cm^2')
    elif FloatArea == 'm^2' and AnswerArea == 'de^2':
        c = a*100
        print('Answer: '+ str(c)+'de^2')
    elif FloatArea == 'm^2' and AnswerArea == 'ap^2':
        c = a*0.01
        print('Answer: '+ str(c)+'ap^2')
    elif FloatArea == 'm^2' and AnswerArea == 'ha^2':
        c = a*0.0001
        print('Answer: '+ str(c)+'ha^2')
    elif FloatArea == 'm^2' and AnswerArea == 'km^2':
        c = a*0.000001
        print('Answer: '+ str(c)+'km^2')
    #ap^2(Сотка)
    if FloatArea == 'ap^2' and AnswerArea == 'mm^2':
        c = a*100000000
        print('Answer: '+ str(c)+'mm^2')
    elif FloatArea == 'ap^2' and AnswerArea == 'cm^2':
        c = a*1000000
        print('Answer: '+ str(c)+'cm^2')
    elif FloatArea == 'ap^2' and AnswerArea == 'de^2':
        c = a*10000
        print('Answer: '+ str(c)+'de^2')
    elif FloatArea == 'ap^2' and AnswerArea == 'm^2':
        c = a*100
        print('Answer: '+ str(c)+'m^2')
    elif FloatArea == 'ap^2' and AnswerArea == 'ha^2':
        c = a*0.01
        print('Answer: '+ str(c)+'ha^2')
    elif FloatArea == 'ap^2' and AnswerArea == 'km^2':
        c = a*0.0001
        print('Answer: '+ str(c)+'km^2')
    #ha^2(Гиктар)
    if FloatArea == 'ha^2' and AnswerArea == 'mm^2':
        c = a*10000000000
        print('Answer: '+ str(c)+'mm^2')
    elif FloatArea == 'ha^2' and AnswerArea == 'cm^2':
        c = a*100000000
        print('Answer: '+ str(c)+'cm^2')
    elif FloatArea == 'ha^2' and AnswerArea == 'de^2':
        c = a*1000000
        print('Answer: '+ str(c)+'de^2')
    elif FloatArea == 'ha^2' and AnswerArea == 'm^2':
        c = a*10000
        print('Answer: '+ str(c)+'m^2')
    elif FloatArea == 'ha^2' and AnswerArea == 'ap^2':
        c = a*100
        print('Answer: '+ str(c)+'ap^2')
    elif FloatArea == 'ha^2' and AnswerArea == 'km^2':
        c = a*0.01
        print('Answer: '+ str(c)+'km^2')
    #km^2
    if FloatArea == 'km^2' and AnswerArea == 'mm^2':
        c = a*1000000000000
        print('Answer: '+ str(c)+'mm^2')
    elif FloatArea == 'km^2' and AnswerArea == 'cm^2':
        c = a*10000000000
        print('Answer: '+ str(c)+'cm^2')
    elif FloatArea == 'km^2' and AnswerArea == 'de^2':
        c = a*100000000
        print('Answer: '+ str(c)+'de^2')
    elif FloatArea == 'km^2' and AnswerArea == 'm^2':
        c = a*1000000
        print('Answer: '+ str(c)+'m^2')
    elif FloatArea == 'km^2' and AnswerArea == 'ap^2':
        c = a*10000
        print('Answer: '+ str(c)+'ap^2')
    elif FloatArea == 'km^2' and AnswerArea == 'ha^2':
        c = a*100
        print('Answer: '+ str(c)+'ha^2')
    #Error Values.
    if (FloatArea == 'mm^2' and AnswerArea == 'mm^2') or (FloatArea == 'cm^2' and AnswerArea == 'cm^2') or (FloatArea == 'de^2' and AnswerArea == 'de^2') or (FloatArea == 'm^2' and AnswerArea == 'm^2') or (FloatArea == 'ap^2' and AnswerArea == 'ap^2') or (FloatArea == 'ha^2' and AnswerArea == 'ha^2') or (FloatArea == 'km^2' and AnswerArea == 'km^2'):
        print("You have selected incorrect values. For example, you can't convert mm^2 to mm^2.")

#VolumeConverter
def VolumeConverterProgram():
    #VolumeController
    #Introduction
    FloatVolume = input("Choose what you want to get the value from(mm^3,cm^3,m^3):")
    a = float(input('Entered value:'))
    AnswerVolume = input("Selest the value you want to convert(mm^3,cm^3,m^3):")
    #mm^3
    if FloatVolume =='mm^3' and AnswerVolume =='cm^3':
        x = a*0.001
        print('Answer: '+ str(x)+'cm^3')
    elif FloatVolume =='mm^3' and AnswerVolume =='m^3':
        x= a*0.000000001
        print('Answer: '+ str(x)+'m^3')
    #cm^3
    if FloatVolume =='cm^3' and AnswerVolume =='mm^3':
        x = a*1000
        print('Answer: '+ str(x)+'mm^3')
    elif FloatVolume =='cm^3' and AnswerVolume =='m^3':
        x= a*0.000001
        print('Answer: '+ str(x)+'m^3')
    #m^3
    if FloatVolume =='m^3' and AnswerVolume =='mm^3':
        x = a*1000000000
        print('Answer: '+ str(x)+'mm^3')
    elif FloatVolume =='m^3' and AnswerVolume =='cm^3':
        x= a*1000000
        print('Answer: '+ str(x)+'cm^3')
    #Error Values.
    if (FloatVolume == 'mm^3' and AnswerVolume == 'mm^3') or (FloatVolume == 'cm^3' and AnswerVolume == 'cm^3') or (FloatVolume == 'm^3' and AnswerVolume == 'm^3'):
        print("You have selected incorrect values. For example, you can't convert mm^3 to mm^3.")

#EnergyConverter(joule)
def EnergyConverterProgram():
    #EnergyController(joule)
    #Introduction       
    FloatEnergy = input("Choose what you want to get the value from(j,kj,mj):")
    a = float(input("Entered value:"))
    AnswerEnergy = input("Selest the value you want to convert(j,kj,mj):")
    #j
    if FloatEnergy =='j' and AnswerEnergy =='kj':
        x = a*0.001
        print('Answer: '+ str(x)+ 'kj')
    elif FloatEnergy =='j' and AnswerEnergy =='mj':
        x = a*0.000001
        print('Answer: '+ str(x)+'mj') 
    #kj
    if FloatEnergy =='kj' and AnswerEnergy =='j':
        x = a*1000
        print('Answer: '+ str(x)+ 'j')
    elif FloatEnergy =='kj' and AnswerEnergy =='mj':
        x = a*0.001
        print('Answer: '+ str(x)+'mj') 
    #mj
    if FloatEnergy =='mj' and AnswerEnergy =='j':
        x = a*1000000
        print('Answer: '+ str(x)+ 'j')
    elif FloatEnergy =='mj' and AnswerEnergy =='kj':
        x = a*1000
        print('Answer: '+ str(x)+'kj')
    #Error Values.
    if ((FloatEnergy =='j' and AnswerEnergy =="j") or (FloatEnergy =='kj' and AnswerEnergy =="kj") or (FloatEnergy =='mj' and AnswerEnergy =="mj")):
        print("You have selected incorrect values. For example, you can't convert j to j!")

#ShortenedConverter
#ShortenedSpeedConverters

#km/h
def kmh_to_mih(x):
    c = x * 0.6
    print(str(c) + 'mi/h.')
def kmh_to_ms(x):
    c = x * 0.28
    print(str(c) + 'm/s.')
#m/s
def ms_to_kmh(x):
    c = x * 3.6
    print(str(c) + 'km/h.')
def ms_to_mih(x):
    c = x * 2.24
    print(str(c) + 'mi/h.')
#mi/h
def mih_to_kmh(x):
    c = x * 1.6
    print(str(c) + 'mi/h.')
def mih_to_ms(x):
    c = x * 0.45
    print(str(c) + 'm/s.')

#ShortenedTimeConverter

#sec
def sec_to_min(x):
    c = x * 0.016
    print(str(c) + 'min.')
def sec_to_h(x):
    c = x * 0.00027
    print(str(c) + 'h.')
def sec_to_d(x):
    c = x * 0.000011
    print(str(c) + 'd.')
#min
def min_to_sec(x):
    c = x * 60
    print(str(c) + 'sec.')
def min_to_h(x):
    c = x * 0.01
    print(str(c) + 'h.')
def min_to_d(x):
    c = x * 0.00069
    print(str(c) + 'd.')
#hours
def h_to_sec(x):
    c = x * 3600
    print(str(c) + 'sec.')
def h_to_min(x):
    c = x * 60
    print(str(c) + 'min.')
def h_to_d(x):
    c = x * 0.0416
    print(str(c) + 'd.')
#day's
def d_to_sec(x):
    c = x * 86400
    print(str(c) + 'sec.')
def d_to_min(x):
    c = x * 1440
    print(str(c) + 'min.')
def d_to_h(x):
    c = x * 24
    print(str(c) + 'h.')

#ShortWeightConverter
#gr
def gr_to_kg(x):
    c = x * 0.001
    print(str(c) + 'kg.')
def gr_to_t(x):
    c = x * 0.000001
    print(str(c) + 't.')
#kg
def kg_to_gr(x):
    c = x * 1000
    print(str(c) + 'gr.')
def kg_to_t(x):
    c = x * 0.001
    print(str(c) + 't.')
#t
def t_to_gr(x):
    c = x * 1000000
    print(str(c) + 'gr.')
def t_to_kg(x):
    c = x * 1000
    print(str(c) + 'kg.')

#ShortLenghtConverter
#mm
def mm_to_cm(x):
    c = x * 0.1
    print(str(c) + 'cm.')
def mm_to_de(x):
    c = x * 0.01
    print(str(c) + 'de.')
def mm_to_in(x):
    c = x * 0.039
    print(str(c) + 'in.')
def mm_to_m(x):
    c = x * 0.001
    print(str(c) + 'm.')
def mm_to_km(x):
    c = x * 0.000001
    print(str(c) + 'km.')
#cm
def cm_to_mm(x):
    c = x * 10
    print(str(c) + 'mm.')
def cm_to_de(x):
    c = x * 0.1
    print(str(c) + 'de.')
def cm_to_in(x):
    c = x * 0.39
    print(str(c) + 'in.')
def cm_to_m(x):
    c = x * 0.01
    print(str(c) + 'm.')
def cm_to_km(x):
    c = x * 0.00001
    print(str(c) + 'km.')
#de
def de_to_cm(x):
    c = x * 10
    print(str(c) + 'cm.')
def de_to_mm(x):
    c = x * 100
    print(str(c) + 'mm.')
def de_to_in(x):
    c = x * 3.937
    print(str(c) + 'in.')
def de_to_m(x):
    c = x * 0.01
    print(str(c) + 'm.')
def de_to_km(x):
    c = x * 0.0001
    print(str(c) + 'km.')
#in
def in_to_cm(x):
    c = x * 2.54
    print(str(c) + 'cm.')
def in_to_de(x):
    c = x * 0.254
    print(str(c) + 'de.')
def in_to_mm(x):
    c = x * 25.4
    print(str(c) + 'mm.')
def in_to_m(x):
    c = x * 0.0254
    print(str(c) + 'm.')
def in_to_km(x):
    c = x * 0.0000254
    print(str(c) + 'km.')
#m
def m_to_cm(x):
    c = x * 100
    print(str(c) + 'cm.')
def m_to_de(x):
    c = x * 10
    print(str(c) + 'de.')
def m_to_in(x):
    c = x * 39.37
    print(str(c) + 'in.')
def m_to_mm(x):
    c = x * 1000
    print(str(c) + 'mm.')
def m_to_km(x):
    c = x * 0.0001
    print(str(c) + 'km.')
#km
def km_to_cm(x):
    c = x * 100000
    print(str(c) + 'cm.')
def km_to_de(x):
    c = x * 10000
    print(str(c) + 'de.')
def km_to_in(x):
    c = x * 39370
    print(str(c) + 'in.')
def km_to_m(x):
    c = x * 1000
    print(str(c) + 'm.')
def km_to_mm(x):
    c = x * 1000000
    print(str(c) + 'mm.')

#ShortTemperatureConverter
#Celsius
def Cels_to_Fahr(c):
    result = (c*1.8+32)
    print(result)
def Cels_to_Kelv(c):
    result = (c+273.15)
    print(result)

#Fahrenheit
def Fahr_to_Cels(f):
    result = ((f-32)/1.8)
    print(result)
def Fahr_to_Kelv(f):
    result = ((f+459.67)/1.8)
    print(result)

#Kelvin
def Kelv_to_Cels(k):
    result = (k-273.15)
    print(result)
def Kelv_to_Fahr(k):
    result = (k*1.8-459.67)  
    print(result) 

#ShortAreaConverter
#mm^2
def mm2_to_cm2(x):
    result = (x*0.01)
    print(result)
def mm2_to_de2(x):
    result = (x*0.0001)
    print(result)
def mm2_to_m2(x):
    result = (x*0.000001)
    print(result)
def mm2_to_ap2(x):
    result = (x*0.00000001)
    print(result)
def mm2_to_ha2(x):
    result = (x*0.0000000001)
    print(result)
def mm2_to_km2(x):
    result = (x*0.000000000001)
    print(result)
#cm^2
def cm2_to_mm2(x):
    result = (x*100)
    print(result)
def cm2_to_de2(x):
    result = (x*0.01)
    print(result)
def cm2_to_m2(x):
    result = (x*0.0001)
    print(result)
def cm2_to_ap2(x):
    result = (x*0.000001)
    print(result)
def cm2_to_ha2(x):
    result = (x*0.00000001)
    print(result)
def cm2_to_km2(x):
    result = (x*0.0000000001)
    print(result)
#de^2
def de2_to_mm2(x):
    result = (x*10000)
    print(result)
def de2_to_cm2(x):
    result = (x*100)
    print(result)
def de2_to_m2(x):
    result = (x*0.01)
    print(result)
def de2_to_ap2(x):
    result = (x*0.0001)
    print(result)
def de2_to_ha2(x):
    result = (x*0.000001)
    print(result)
def de2_to_km2(x):
    result = (x*0.00000001)
    print(result)
#m^2
def m2_to_mm2(x):
    result = (x*1000000)
    print(result)
def m2_to_cm2(x):
    result = (x*10000)
    print(result)
def m2_to_de2(x):
    result = (x*100)
    print(result)
def m2_to_ap2(x):
    result = (x*0.01)
    print(result)
def m2_to_ha2(x):
    result = (x*0.0001)
    print(result)
def m2_to_km2(x):
    result = (x*0.000001)
    print(result)
#ap^2(сотка)
def ap2_to_mm2(x):
    result = (x*100000000)
    print(result)
def ap2_to_cm2(x):
    result = (x*1000000)
    print(result)
def ap2_to_de2(x):
    result = (x*10000)
    print(result)
def ap2_to_m2(x):
    result = (x*100)
    print(result)
def ap2_to_ha2(x):
    result = (x*0.01)
    print(result)
def ap2_to_km2(x):
    result = (x*0.0001)
    print(result)
#ha^2(гиктар)
def ha2_to_mm2(x):
    result = (x*10000000000)
    print(result)
def ha2_to_cm2(x):
    result = (x*100000000)
    print(result)
def ha2_to_de2(x):
    result = (x*1000000)
    print(result)
def ha2_to_m2(x):
    result = (x*10000)
    print(result)
def ha2_to_ap2(x):
    result = (x*100)
    print(result)
def ha2_to_km2(x):
    result = (x*0.01)
    print(result)
#km^2
def km2_to_mm2(x):
    result = (x*1000000000000)
    print(result)
def km2_to_cm2(x):
    result = (x*10000000000)
    print(result)
def km2_to_de2(x):
    result = (x*100000000)
    print(result)
def km2_to_m2(x):
    result = (x*1000000)
    print(result)
def km2_to_ap2(x):
    result = (x*10000)
    print(result)
def km2_to_ha2(x):
    result = (x*100)
    print(result)

#ShortVolumeConverter
#Volume
#mm^3
def mm3_to_cm3(x):
    result = (x*0.001)
    print(result)
def mm3_to_m3(x):
    result = (x*0.000000001)
    print(result)
#cm^3
def cm3_to_mm3(x):
    result = (x*1000)
    print(result)
def cm3_to_m3(x):
    result = (x*0.000001)
    print(result)
#m^3
def m3_to_mm3(x):
    result = (x*1000000000)
    print(result)
def m3_to_cm3(x):
    result = (x*1000000)
    print(result)

#ShortEnergyConverter
#j
def j_to_kj(x):
    result = (x*0.001)
    print(result)
def j_to_mj(x):
    result = (x*0.000001)
    print(result)
#kj
def kj_to_j(x):
    result = (x*1000)
    print(result)
def kj_to_mj(x):
    result = (x*0.001)
    print(result)
#mj
def mj_to_j(x):
    result = (x*1000000)
    print(result)
def mj_to_kj(x):
    result = (x*1000)
    print(result)
#The End!