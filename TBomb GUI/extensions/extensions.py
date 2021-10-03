import tkinter as tk
from sys import exit as sys_exit
from tkinter.messagebox import showinfo
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils.provider import APIProvider
from time import strftime
from threading import Thread
from requests import get as requests_get

class BomberStatus( tk.Toplevel):
	
	def __init__(self, parent ):
		tk.Toplevel.__init__(self,parent)

		self.geometry("500x400")

		self.text = tk.Text(self)
		self.text.pack(fill='both', expand=1)

	def write(self, chars, **kwargs):
		self.text.configure(**kwargs)
		self.text.insert(tk.END, "\n"+chars)
		self.update()

	def workernode(self, mode, cc_phone, n_sms, delay, max_threads):
		api = APIProvider(cc_phone[0], cc_phone[1], mode, delay=delay)
		msg=f"""
 Gearing up the Bomber - Please be patient\nPlease stay connected to the internet during bombing")
    
		    API Version  : {api.api_version}
		    Target       : {cc_phone[0] + cc_phone[1] }
		    Amount       : {str(n_sms)}
		    Threads      : {str(max_threads)} threads 
		    Delay        : {str(delay)} seconds

This tool was made for fun and research purposes only."""
		self.write(msg)
		if len(APIProvider.api_providers) == 0:
			self.write("Your country/target is not supported yet")
			self.write("Feel free to reach out to us")
			sys_exit()

		success, failed =  0,0
		self.write(f"Target: {cc_phone[0]+cc_phone[1]}",**{"fg":"red"})
		while success < n_sms:
			with ThreadPoolExecutor(max_workers=max_threads) as executor:
				jobs = []
				for i in range(n_sms-success):
					jobs.append(executor.submit(api.hit))
			for job in as_completed(jobs):
				result = job.result()
				
				if result is None:
					self.write( "Bombing limit for your target has been reached")
					self.write("Try Again Later !!... exiting now")
					sys.exit()
				if result:
					success += 1
				else:
					failed += 1 

				self.write(f"{ self.get_time()} >  Success :{success} |  Failed :{failed} ")
				
			self.write("\n")
		self.write("<<<<<<<<<<<  Bombing completed!  >>>>>>>>>>>>",**{"fg":"black"})
		sys_exit()

	def get_time(self): return strftime("%I:%M:%S")

	def check_internet(self):
		try:
			requests_get("https://www.google.com")
			self.write("Internet connection Available...", **{"fg":"green"})
		except:
			self.write("No internet connection Available...",**{"fg":"red"})
			sys_exit(2)

	def selectnode(self, mode, cc_phone, n_sms, delay, n_threads):
	    mode = mode.lower().strip()
	    try:
	        self.write("Checking internet connection...", **{"fg":"blue"})
	        self.check_internet()

	        max_limit = {"sms": 500, "call": 15, "mail": 200}

	        cc, target = "", ""

	        if mode in ["sms", "call"]:
	            cc, target = cc_phone
	            if cc != "91":
	                max_limit.update({"sms": 100})
	        elif mode == "mail":
	            target = get_mail_info(cc_phone[1])
	        else:
	            raise KeyboardInterrupt

	        limit = max_limit[mode]
	        while True:
	            try:
	                if n_sms > limit or n_sms == 0:
	                    self.write("You have requested " + str(n_sms)
	                                            + " {type}".format(
	                                                type=mode.upper()))
	                    self.write(
	                        "Automatically capping the value"
	                        " to {limit}".format(limit=limit))
	                    n_sms = limit
	                # delay = 0
	                max_thread_limit = (n_sms//10) if (n_sms//10) > 0 else 1

	                n_threads = n_threads if (
	                    n_threads > 0) else max_thread_limit
	                if (n_sms < 0 or delay < 0):
	                    raise Exception
	                break
	            except KeyboardInterrupt as ki:
	                raise ki
	                break
	            except Exception as e:
	                self.write("Read Instructions Carefully !!!", e)
	                break

	        return self.workernode(mode, cc_phone,n_sms,delay,n_threads)
	    except KeyboardInterrupt:
	        self.write("Received INTR call - Exiting...")
	        sys_exit()

	def get_mail_info(self, target):
		mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		while True:
			if not re.search(mail_regex, target, re.IGNORECASE):
				msg = (False,"The mail ({target})".format(target=target) + " that you have entered is invalid")
				continue
			return msg + (target, )












class OPButtons(tk.Frame):
	def __init__(self, parent, lbl, img, descpn,command, *args, **kwargs):
		tk.Frame.__init__(self, parent,*args,**kwargs)

		self.img = tk.PhotoImage(file=img)

		self.logo = tk.Label(self, image=self.img, bd=0)
		self.logo.pack(side='left', fill='y',padx=10, pady=10)

		container = tk.Frame(self,height=120,width=460, padx=15, pady=15)
		container.pack(side='right', fill='both', expand=1)

		l1 = tk.Label(container, text=lbl, font=("",15))
		l1.place(x=0, y=0)
		l2 = tk.Label(container, text=descpn,justify="left",font=("",9))
		l2.place(x=0, y=30)

		self.btn  = tk.Button(container, bd=0, fg='blue', text=f'Start {lbl.lower()}' , command=command)
		self.btn.place(x=290, y=70)

		self.wids  =  [self, self.logo, container, l1, l2 ,self.btn ]

		self.hover_out(None)

		self.bind("<Enter>", self.hover_in)
		self.bind("<Leave>", self.hover_out)
	def hover_in(self, e=None):
		for w in self.wids: w['bg'] = '#ccc'
	def hover_out(self, e):
		for w in self.wids: w['bg'] = '#ddd'

class LabeledEntry(tk.LabelFrame):
	""" just like labeledEntry but having a bottom label to display any alert or messages 
		lbltext =>  for entry box title
		imglocation => to display any icon (pass location of image only)
		"""
	def __init__(self,parent, lbltext,imglocation='',*args, **kwargs):
		tk.LabelFrame.__init__(self,parent,*args, **kwargs)
		self.configure(text="     ",bd=0)

		self.lbltext = lbltext
		self.entryVar=tk.StringVar()
		self.entryVar.set(lbltext)
		#get parent frame color
		colr = self['bg']
		#label to diaplay input box icon
		self.imglbl=tk.Label(self,anchor='nw', **kwargs)
		self.entry = tk.Entry(self,textvariable=self.entryVar,fg='#999', bd=0,font=('Arial',11), width=18,**kwargs)
		self.entry['bg']=colr
		#to display messages on the bottom is anu error occurs 
		#to create bottom line effect 
		self.lining = tk.Frame(self,relief='raised',bg='black')
	

		if imglocation!='':
			self.im=tk.PhotoImage(file=imglocation)
			self.imglbl['image']=self.im
			self.imglbl.image=self.im
		#bind functions
		self.entry.bind('<FocusIn>',self.Focusin)
		self.entry.bind('<FocusOut>',self.FocusOut)
		#pack widgets
		self.lining.pack(side='bottom',fill='x',anchor='nw', expand=1)
		self.imglbl.pack(anchor='nw',side='left')
		self.entry.pack(fill='both',expand=1,anchor='nw')

	def get(self):
		return self.entryVar.get().strip()

	def Focusin(self,event):
		#if input box gets the focus claer alert message
		if self.get() == self.lbltext:
			self.entryVar.set("")
			self['text']= self.lbltext
			self.entry['fg'] = "#000"
			
	def FocusOut(self,e):
		if self.get() == "":
			self["text"] = "     "
			self.entry['fg'] = "#999"
			self.entryVar.set(self.lbltext)


class  EmailBombing(tk.Frame):
	"""docstring for  EmailBombing"""
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.cl = tk.PhotoImage(file="./media/close.png")

		tk.Label(self, text='This Option \nWill Be\n Available \nSoon!',fg='red', font=("", 40)).pack()
		self.back_button = tk.Button(self, image=self.cl, bd=0)
		self.back_button.place(x=520,y=5)
		

class CallBombingUI( tk.Frame ):
	def __init__(self, parent, bombing_mode):
		tk.Frame.__init__(self, parent)

		self.bombing_mode = bombing_mode
		self.cl = tk.PhotoImage(file="./media/close.png")

		tk.Label(self, text="{} Bombing".format(self.bombing_mode.upper()),bd=0, font=("",45)).place(x=5,y=10)

		self.back_button = tk.Button(self, image=self.cl, bd=0)
		self.back_button.place(x=520,y=5)


		self.c_code = LabeledEntry(self,"Your country code (Without +)")
		self.c_code.entry['width'] = 50
		self.c_code.place(x=80, y=100)

		self.mn = LabeledEntry(self,"Target mobile number")
		self.mn.entry['width'] = 50
		self.mn.place(x=80, y=170)

		self.n_sms_or_call = LabeledEntry(self,"Number of {} to send (Max 500)".format(self.bombing_mode.upper()))
		self.n_sms_or_call.entry['width'] = 50
		self.n_sms_or_call.place(x=80, y=240)

		self.delay = LabeledEntry(self,"Delay time (in seconds)")
		self.delay.entry['width'] = 50
		self.delay.place(x=80, y=310)

		self.n_threads = LabeledEntry(self,"Number of Thread (Recommended: 1)")
		self.n_threads.entry['width'] = 50
		self.n_threads.place(x=80, y=390)

		self.start_btn = tk.Button(self,text="Start", bd=1, relief="ridge",font=("",12), padx=50,fg="blue",command=self.confirm_bombing_details)
		self.start_btn.place(x=200, y= 450,)


	def confirm_bombing_details(self):
		from tkinter.messagebox import askyesno

		ans = askyesno(title="Gearing up the Bomber..",
			message=f"""
Please stay connected to the internet during bombing

	API Version	: 2.3
	Target		: {self.mn.get()}
	Amount		: {self.n_sms_or_call.get()}
	Threads		: {self.n_threads.get()}
	Delay		: {self.delay.get()} seconds
This tool was made for fun and research purposes only
			""", detail="Do you wish to continue?")


		if ans:
			new = BomberStatus(self)
			
			ret = Thread( target = new.selectnode, daemon=True,
				args=(
					self.bombing_mode,  
					( self.c_code.get(), self.mn.get() ),
					int(self.n_sms_or_call.get()), 
					int(self.delay.get()), 
					int(self.n_threads.get())
				))
			ret.start()
		else:
			pass


	def start_bombing(self):
		pass