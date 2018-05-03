from __future__ import print_function  
import remi.gui as gui 
from remi.gui import * 
from remi import start, App 
from threading import Timer 
import hid  
import time  
import serial 
import struct 
import numpy as np 
from datetime import datetime, date, time 
from time import sleep 
import pandas as pd 
from pandas import ExcelWriter 
from pandas import ExcelFile 
 
data = serial.Serial(port='/dev/cu.SLAB_USBtoUART', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1) 
print("connected to: " + data.portstr) 

start_time = 0
start_time_second = 0
start_time_minute = 0
start_time_hour = 0
total_start_time = 0

target_temp1 = 0
target_temp2 = 0

instructions = 0
step = 0

heater1 = True
heater2 = True

first_loop = True

class MyApp(App):
        def __init__(self, *args):
                super(MyApp, self).__init__(*args, static_file_path='./res/')

        def main(self):
                verticalContainer = gui.Widget(style={'width': '100%', 'height': '100%','display': 'block', 'overflow': 'auto', 'text-align': 'center', 'background-color': '#2F4F4f', 'border-color': 'black', 'border-width': '2px', 'border-style' : 'solid', 'left':'20%' })


                self.close = gui.Button('Reset',  style = {'width':'16%', 'color' :'black', 'background-color' :'red', 'font-size' : '2.5vw',  'height':'8.0%', 'left': '75%', 'margin':'auto', 'top': '87%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
                self.close.set_on_click_listener(self.on_button_pressed)


                self.fire_img = gui.Image('res/fire.png', style = {'width':'16%', 'height':'8.0%', 'left': '6.5%', 'margin':'auto', 'top': '52%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
                self.kettle_img = gui.Image('res/kettle.png', style = {'width':'17.0%', 'height':'25.0%', 'left': '8%', 'margin':'auto', 'top': '32%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.kettle_img2 = gui.Image('res/second_kettle.png', style = {'width':'17.0%', 'height':'28.0%', 'left': '28%', 'margin':'auto', 'top': '34%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.kettle_img3 = gui.Image('res/monk-brewing-beer.png', style = {'width':'12.0%', 'height':'27.0%', 'left': '54%', 'margin':'auto', 'top': '31%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.kettle_img4 = gui.Image('res/beer_barrel.png', style = {'width':'17.0%', 'height':'23.0%', 'left': '74%', 'margin':'auto', 'top': '65%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.fire_img1 = gui.Image('res/blank.png', style = {'width':'16%', 'height':'8.0%', 'left': '50.5%', 'margin':'auto', 'top': '52%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
                self.water_pump1 = gui.Image('res/pump_static.png', style = {'width':'7.0%', 'height':'8.50%', 'left': '29%', 'margin':'auto', 'top': '60%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.water_pump2 = gui.Image('res/pump_static.png', style = {'width':'7.0%', 'height':'8.50%', 'left': '49%', 'margin':'auto', 'top': '60%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.water_pump3 = gui.Image('res/pipes.gif', style = {'width':'19.0%', 'height':'35.0%', 'left': '37.5%', 'filter':'flipH', 'margin':'auto', 'top': '33.5%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.water_pump4 = gui.Image('res/pipes.gif', style = {'width':'19.0%', 'height':'35.0%', 'left': '37.5%', 'filter':'flipH', 'margin':'auto', 'top': '33.5%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.heat_exchanger = gui.Image('res/heat_exchanger.png', style = {'width':'9.0%', 'height':'10.50%', 'left': '69%', 'margin':'auto', 'top': '58%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.faucet = gui.Image('res/blank.png', style = {'width':'7.0%', 'height':'8.50%', 'left': '65%', 'margin':'auto', 'top': '66%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.cup = gui.Image('res/blank.png', style = {'width':'8.0%', 'height':'8.0%', 'left': '48%', 'margin':'auto', 'top': '28%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.sign = gui.Image('res/sign2.png', style = {'width':'28.0%', 'height':'24.0%', 'left': '36%', 'margin':'auto', 'top': '72%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.pipe = gui.Image('res/pipe-only1.png', style = {'width':'14.0%', 'height':'24.0%', 'left': '59%', 'margin':'auto', 'top': '48%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
                self.pipe_right = gui.Image('res/pipes-right-only-static.png', style = {'width':'19.0%', 'height':'35.0%', 'left': '17.5%', 'filter':'flipH', 'margin':'auto', 'top': '33.5%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})


                self.counter = gui.Label('', style = {'width' : '24%', 'height' : '10%', 'padding-top' : '1%', 'color': 'green', 'left' : '3%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '2.5vw', 'top' : '82%', 'text-align':'center', 'z-index' : '0'})

                self.target_temp1 = gui.Label(' Target temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'red', 'left' : '3%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '12%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
                self.target_temp1_val = gui.TextInput(style = {'width' : '8%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '16%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '12%', 'text-align':'left', 'padding-left': '0%', 'z-index' : '1'})
                self.target_temp1_val.set_text('250 \u2103')

                self.current_temp1 = gui.Label(' Current temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': '#75e7ff', 'left' : '3%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '22%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
                self.current_temp1_val = gui.Label('0 \u2103', style = {'width' : '8%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '16%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '22%', 'text-align':'left', 'padding-left': '0%', 'z-index' :'1'})


                self.target_temp2 = gui.Label(' Target temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'red', 'left' : '51%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '12%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
                self.target_temp2_val = gui.TextInput(style = {'width' : '8%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '64%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '12%', 'text-align':'left', 'padding-left': '0%', 'z-index' : '1'})
                self.target_temp2_val.set_text('100 \u2103')

                self.current_temp2 = gui.Label(' Current temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': '#75e7ff', 'left' : '51%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '22%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
                self.current_temp2_val = gui.Label('0 \u2103', style = {'width' : '8%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '64%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '22%', 'text-align':'left', 'padding-left': '0%', 'z-index' :'1'})

                self.current_task = gui.Label(' Current Task:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '12%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
                self.current_task_val = gui.Label('Pending', style = {'width' : '20%', 'height' : '14%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '0.8%', 'z-index' :'1'})


                self.target_time = gui.Label(' Target time:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '32%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
                self.target_time_val = gui.TextInput(style = {'width' : '8%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '86%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '32%', 'text-align':'left', 'padding-left': '0%', 'z-index' : '1'})


                self.current_time = gui.Label(' Time left:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '32%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})

                self.current_time_val = gui.Label('00:00:00', style = {'width' : '8%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '86%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '32%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})


                self.get_time()
                delta_time = self.get_time()
                self.counter.set_text('Running Time: ' + str(int(delta_time/3600)).zfill(2)+":"+ str(int(delta_time/60)%60).zfill(2)+":"+str(delta_time%60).zfill(2))
                verticalContainer.append(self.target_temp1)
                verticalContainer.append(self.current_temp1)
                verticalContainer.append(self.target_temp1_val)
                verticalContainer.append(self.current_temp1_val)
                #verticalContainer.append(self.target_time)
                #verticalContainer.append(self.target_time_val)
                verticalContainer.append(self.current_time)
                verticalContainer.append(self.current_time_val)
                verticalContainer.append(self.target_temp2)
                verticalContainer.append(self.current_temp2)
                verticalContainer.append(self.target_temp2_val)
                verticalContainer.append(self.current_temp2_val)
                verticalContainer.append(self.current_task)
                verticalContainer.append(self.current_task_val)
                verticalContainer.append(self.fire_img)
                verticalContainer.append(self.fire_img1)
                verticalContainer.append(self.kettle_img)
                verticalContainer.append(self.kettle_img2)
                verticalContainer.append(self.kettle_img3)
                verticalContainer.append(self.kettle_img4)
                verticalContainer.append(self.water_pump1)
                verticalContainer.append(self.water_pump2)
                verticalContainer.append(self.water_pump3)
                verticalContainer.append(self.water_pump4)
                verticalContainer.append(self.pipe)
                verticalContainer.append(self.pipe_right)
                verticalContainer.append(self.heat_exchanger)
                verticalContainer.append(self.faucet)
                verticalContainer.append(self.counter)
                verticalContainer.append(self.cup)
                verticalContainer.append(self.sign)
                verticalContainer.append(self.close)

                # kick of regular display of counter
                self.run_brewery()

                # returning the root widget
                return verticalContainer


        def get_time(self):
                global start_time_second
                global start_time_minute
                global start_time_hour
                global total_start_time

                current_time = datetime.now()
                current_time_second = current_time.second
                current_time_minute = current_time.minute
                current_time_hour = current_time.hour
                total_current_time = current_time.second + 60*current_time.minute + 3600*current_time.hour

                if (total_current_time < total_start_time):
                        total_current_time += 12*3600

                delta_time = total_current_time - total_start_time

                return delta_time

        def on_button_pressed(self, _):
                print("3\n3\n3\n\n3\n3\n3\n")
                global delta_pump_time
                global first_loop


                global start_time
                global start_time_second
                global start_time_minute
                global start_time_hour
                global total_start_time
		
                global step
                global target_temp1
                global target_temp2

                step = 0

                target_temp1 = -999
                target_temp2 = -999
                start_time = datetime.now()
                start_time_second = start_time.second
                start_time_minute = start_time.minute
                start_time_hour = start_time.hour
                total_start_time = start_time_second + 60*start_time_minute+3600*start_time_hour
                delta_time = self.get_time()
                self.counter.set_text('Running Time: ' + str(int(delta_time/3600)).zfill(2)+":"+ str(int(delta_time/60)%60).zfill(2)+":"+str(delta_time%60).zfill(2))


                first_loop = True

                self.current_time_val.set_text('00:00:00')
                self.target_temp1_val.set_text('250 \u2103')
                self.target_temp2_val.set_text('100 \u2103')
                h.write([0x00,0xfc])
                self.fire_img.set_image('res/fire.png')
                self.kettle_img.set_image('res/kettle.png')
                self.kettle_img2.set_image('res/second_kettle.png')
                self.kettle_img3.set_image('res/monk-brewing-beer.png')
                self.kettle_img4.set_image('res/beer_barrel.png')
                self.fire_img1.set_image('res/blank.png')
                self.water_pump1.set_image('res/pump_static.png')
                self.water_pump2.set_image('res/pump_static.png')
                self.water_pump3.set_image('res/pipes.gif')
                self.water_pump4.set_image('res/pipes.gif')
                self.heat_exchanger.set_image('res/heat_exchanger.png')
                self.faucet.set_image('res/blank.png')
                self.cup.set_image('res/blank.png')
                self.sign.set_image('res/sign2.png')
                self.pipe.set_image('res/pipe-only1.png')
                self.pipe_right.set_image('res/pipes-right-only-static.png')
                self.turn_off_pump1()
                self.turn_off_pump2()
                self.turn_off_pump3()
                self.turn_off_pump4()
                self.turn_off_faucet()
                self.run_brewery()


        def maintain_temp(self, target_temp1,target_temp2):
                global heater1, heater2
                data.write(struct.pack('>B',90))
                current_temp1 = 0
                current_temp2 = 0
                try:
                        current_temp1 = float((data.readline()).decode('UTF-8')[-8:-1])
                        current_temp2 = float((data.readline()).decode('UTF-8')[-8:-1])
                        data.readline()
                        self.current_temp1_val.set_text(str(temp1)+"\u2103")
                        self.current_temp2_val.set_text(str(temp2)+"\u2103")
                except:
                        print("Error Reading Temp")
                if current_temp1 < target_temp1 and heater1 == False:
                        heater1 = True
                        self.fire_img.set_image('res/fire.png')
                        try:
                                # turn heater 1 on
                                print("Turning on heater 1")
                                h.write([0x00,0xff,0x01])
                        except IOError as ex:
                                print(ex)
                                print("You probably don't have the hard coded device. Update the hid.device line")
                                print("in this script with one from the enumeration list output above and try again.")
                if current_temp1 >= target_temp1 and heater1 == True:
                        heater1 = False
                        self.fire_img.set_image('res/blank.png')
                        try:
                                # turn heater 1 on
                                print("Turning off heater 1")
                                h.write([0x00,0xfd,0x01])
                        except IOError as ex:
                                print(ex)
                                print("You probably don't have the hard coded device. Update the hid.device line")
                                print("in this script with one from the enumeration list output above and try again.")


                if current_temp2 < target_temp2 and heater2 == False:
                        heater2 = True
                        self.fire_img1.set_image('res/fire.png')
                        try:
                                # turn heater 1 on
                                print("Turning on heater 2")
                                h.write([0x00,0xff,0x05])
                        except IOError as ex:
                                print(ex)
                                print("You probably don't have the hard coded device. Update the hid.device line")
                                print("in this script with one from the enumeration list output above and try again.")
                if current_temp2 >= target_temp2 and heater2 == True:
                        heater2 = False
                        self.fire_img1.set_image('res/blank.png')
                        try:
                                # turn heater 1 on
                                print("Turning off heater 2")
                                h.write([0x00,0xfd,0x05])
                        except IOError as ex:
                                print(ex)
                                print("You probably don't have the hard coded device. Update the hid.device line")
                                print("in this script with one from the enumeration list output above and try again.")



        def set_temp1(self):
                global target_temp1
                current_temp1 = 0
                current_temp2 = 0
                self.fire_img.set_image('res/fire.png')
                try:
                        # turn heater 1 on
                        print("Turning on heater 1")
                        h.write([0x00,0xff,0x01])
                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

                while current_temp1 < target_temp1:
                        data.write(struct.pack('>B',90))
                        try:
                                current_temp1 = float((data.readline()).decode('UTF-8')[-8:-1])
                                current_temp2 = float((data.readline()).decode('UTF-8')[-8:-1])
                                data.readline()
                                self.current_temp1_val.set_text(str(temp1)+"\u2103")
                                self.current_temp2_val.set_text(str(temp2)+"\u2103")
                        except:
                                print("Error Reading Temp")
                        sleep(1)

                return target_temp1


        def set_temp2(self):
                global target_temp2
                current_temp1 = 0
                current_temp2 = 0
                self.fire_img1.set_image('res/fire.png')
                try:
                        # turn heater 1 on
                        print("Turning on heater 2")
                        h.write([0x00,0xff,0x05])
                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")
                while current_temp1 < target_temp1:
                        data.write(struct.pack('>B',90))
                        try:
                                current_temp1 = float((data.readline()).decode('UTF-8')[-8:-1])
                                current_temp2 = float((data.readline()).decode('UTF-8')[-8:-1])
                                data.readline()
                                self.current_temp1_val.set_text(str(temp1)+"\u2103")
                                self.current_temp2_val.set_text(str(temp2)+"\u2103")
                        except:
                                print("Error Reading Temp")
                        sleep(1)

                return target_temp2

        def turn_on_pump1(self):
                try:
                        #turn pump 1 on
                        print("Turning on pump 1")
                        h.write([0x00,0xff,0x02])
                        self.water_pump1.set_image('res/Wassermotor-mit_Pfeilen_w_trans4.png.gif')
                        self.pipe_right.set_image('res/pipes-right-only.gif')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_off_pump1(self):
                try:
                        #turn pump 1 off
                        print("Turning off pump 1")
                        h.write([0x00,0xfd,0x02])
                        self.pipe_right.set_image('res/pipes-right-only-static.png')
                        self.water_pump1.set_image('res/pump_static.png')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_on_pump2(self):
                try:
                        #turn pump 1 on
                        print("Turning on pump 2, path 1")
                        h.write([0x00,0xff,0x03])
                        self.water_pump2.set_image('res/Wassermotor-mit_Pfeilen_w_trans4.png.gif')
                        self.water_pump3.set_image('res/pipes-left.gif')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_off_pump2(self):
                try:
                        #turn pump 1 off
                        print("Turning off pump 2, path 1")
                        h.write([0x00,0xfd,0x03])
                        self.water_pump2.set_image('res/pump_static.png')
                        self.water_pump3.set_image('res/pipes.gif')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_on_pump3(self):
                try:
                        #turn pump 1 on
                        print("Turning on pump 2, path 2")
                        h.write([0x00,0xff,0x04])
                        self.water_pump2.set_image('res/Wassermotor-mit_Pfeilen_w_trans4.png.gif')
                        self.water_pump4.set_image('res/pipes-right.gif')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_off_pump3(self):
                try:
                        #turn pump 1 off
                        print("Turning off pump 2, path 2")
                        h.write([0x00,0xfd,0x04])
                        self.water_pump2.set_image('res/pump_static.png')
                        self.water_pump4.set_image('res/pipes.gif')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")
                        print("Turning off pump 1")

        def turn_on_pump4(self):
                try:
                        #turn pump 3 on
                        print("Turning on pump 4")
                        h.write([0x00,0xff,0x06])

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_off_pump4(self):
                try:
                        #turn pump 3 on
                        print("Turning off pump 4")
                        h.write([0x00,0xfd,0x06])

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_on_faucet(self):
                try:
                        #turn pump 3 on
                        print("Turning on faucet")
                        h.write([0x00,0xff,0x07])
                        self.pipe.set_image('res/pipe-only1.gif')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")


        def turn_off_faucet(self):
                try:
                        #turn pump 3 on
                        print("Turning off faucet")
                        h.write([0x00,0xfd,0x07])
                        self.pipe.set_image('res/pipe-only1.png')

                except IOError as ex:
                        print(ex)
                        print("You probably don't have the hard coded device. Update the hid.device line")
                        print("in this script with one from the enumeration list output above and try again.")

        def turn_cup(self):
                data.write(struct.pack('>B',0))
                self.cup.set_image('res/cup.gif')
                sleep(5)
                self.cup.set_image('res/blank.png')
                data.write(struct.pack('>B',90))

        def wait(self,target_time):
                global first_loop
                global target_temp1
                global target_temp2
                if first_loop == True:
                        start_time = self.get_time()
                        delta_time = self.get_time()-start_time
                        first_loop == False
                while (delta_time < target_time):
                        delta_time = self.get_time()-start_time
                        self.maintain_temp(target_temp1, target_temp2)
                        if (target_time-delta_time) < 0:
                                self.current_time_val.set_text('00:00:00')
                        else:
                                self.current_time_val.set_text(str(int((target_time-delta_time)/3600)).zfill(2)+":"+ str(int((target_time-delta_time)/60)%60).zfill(2)+":"+str((target_time-delta_time)%60).zfill(2))
                        running_time = self.get_time()
                        self.counter.set_text('Running Time: ' + str(int(running_time/3600)).zfill(2)+":"+ str(int(running_time/60)%60).zfill(2)+":"+str(running_time%60).zfill(2))
                        sleep(1)

        def run_brewery(self):
                global target_temp1, target_temp2, instructions, step, start_time, total_start_time
                DESCRIPTOR = instructions['DESCRIPTOR'][step]
                ID = int(instructions['ID'][step])
                ARG = instructions['ARGUMENT'][step]

                self.current_task_val.set_text(str(DESCRIPTOR))

                delta_time = self.get_time()
                self.counter.set_text('Running Time: ' + str(int(delta_time/3600)).zfill(2)+":"+ str(int(delta_time/60)%60).zfill(2)+":"+str(delta_time%60).zfill(2))
                print(step)

                if ID == 0:
                        self.wait(int(ARG))
                        self.target_time_val.set_text(str(int(ARG/3600)).zfill(2)+":"+ str(int(ARG/60)%60).zfill(2)+":"+str(ARG%60).zfill(2))
                if ID == 1:
                        self.turn_on_pump1()
                if ID == 2:
                        self.turn_off_pump1()
                if ID == 3:
                        self.turn_on_pump2()
                if ID == 4:
                        self.turn_off_pump2()
                if ID == 5:
                        self.turn_on_pump3()
                if ID == 6:
                        self.turn_off_pump3()
                if ID == 7:
                        self.turn_on_pump4()
                if ID == 8:
                        self.turn_off_pump4()
                if ID == 9:
                        target_temp1 = float(ARG)
                        self.target_temp1_val.set_text(str(target_temp1))
                        self.set_temp1()
                if ID == 10:
                        target_temp2 = float(ARG)
                        self.target_temp2_val.set_text(str(target_temp2))
                        self.set_temp2()
                if ID == 11:
                        self.turn_cup()
                if ID == 12:
                        self.turn_on_faucet()
                if ID == 13:
                        self.turn_off_faucet()
                self.maintain_temp(target_temp1, target_temp2)
	
                print(step)
                if step < len(instructions['ID']):
                        step+=1
                if step == len(instructions['ID']):
                        self.current_task_val.set_text("DONE!\nHOPE YOU ENJOY THE BEER!")
                Timer(1, self.run_brewery).start()

if __name__ == "__main__":
        global start_time
        global start_time_second
        global start_time_minute
        global start_time_hour
        global total_start_time

        start_time = datetime.now()
        start_time_second = start_time.second
        start_time_minute = start_time.minute
        start_time_hour = start_time.hour
        total_start_time = start_time_second + 60*start_time_minute+3600*start_time_hour

        print("Opening the device")
        h = hid.device()
        h.open(5824, 1503) # trezor vendorid/productid

        print("Manufacturer: %s" % h.get_manufacturer_string())
        print("Product: %s" % h.get_product_string())
        print("Serial No: %s" % h.get_serial_number_string())

        # enable non-blocking mode
        h.set_nonblocking(1)

        h.write([0x00,0xfc])

        filename = input("Enter a filename: ")
        instructions = pd.read_excel('brewing_instructions.xlsx', sheetname='Sheet1')
        start(MyApp, debug=True, address='0.0.0.0', port = 5000, start_browser=True)

        h.write([0x00,0xfc])
        print("Closing the device")
        h.close()
        ser.close()


