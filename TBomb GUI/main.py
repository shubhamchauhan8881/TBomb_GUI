import tkinter as tk
from extensions import extensions as extn
from webbrowser import open_new_tab as web_open
class MmainWindow( tk.Tk ):
	PACKED_WINDOWS = []

	def __init__(self, parent=None):
		tk.Tk.__init__(self, parent)
		self.icon  = tk.PhotoImage(file='./media/tbomb_logo.png')
		self.geometry("780x520+250+100")
		self.resizable(0,0)
		self.title("TBomb")
		self.iconphoto(False, self.icon)
		
		self.TBomb()
		self.UI()

		self.CALL_BOMBING_WIN = extn.CallBombingUI(self,"call")
		self.SMS_BOMBING_WIN = extn.CallBombingUI(self,"sms")
		self.EMAIL_BOMBING_WIN = extn.EmailBombing(self)


		self.CALL_BOMBING_WIN.back_button['command'] = self.go_back_to_home
		self.SMS_BOMBING_WIN.back_button['command'] = self.go_back_to_home
		self.EMAIL_BOMBING_WIN.back_button['command'] = self.go_back_to_home


	def TBomb(self):
		self.lft = tk.Frame(self, bg='#ddd', padx=5)
		self.lft.pack(side="left", fill='y', )

		self.lbl = tk.Label(self.lft, image=self.icon, bg='#ddd',text=f"Version : {self.get_version()}" ,compound="top")
		self.lbl.pack(pady=15)

		tk.Button(self.lft, text='Designed by Elsker Elvish',command= web_open("https://www.instagram.com/elsker_elvish.py/") , bd=0, bg='#ddd').pack(side="bottom", fill='x')	
		tk.Button(self.lft, text='Check For Updates..',command=self.not_avail,fg='blue', bd=0, bg='#ddd').pack(side="bottom", fill='x')
		tk.Button(self.lft, text='GitHub link..',command=lambda : web_open("https://github.com/ElskerElvish/TBomb_GUI"),fg='blue', bd=0, bg='#ddd').pack(side="bottom", fill='x')
		tk.Button(self.lft, text='About..',command=self.not_avail,fg='blue', bd=0, bg='#ddd').pack(side="bottom", fill='x')
	
	def not_avail(self):
		print("Currently unavailable....")
	
	def UI(self):		
		self.mainF = tk.Frame(self)

		title = tk.Label(self.mainF, text="TBomb", fg='black', font = ("",45))
		title.place(x=0, y=10)

		lil_descpn = tk.Label(self.mainF, text="A free and open-source SMS/Call bombing application.", font=("",11))
		lil_descpn.place(x=0, y=90)

		call = extn.OPButtons(self.mainF, "Call Bombing","./media/phone.png", "Phone bombing..\nSend spand calls to your friend have fun!", lambda : self.window_packer(self.CALL_BOMBING_WIN))
		call.place(x=10,y=130)

		sms = extn.OPButtons(self.mainF, "SMS Bombing","./media/sms.png", "SMS bombing..\nSend spand messages to your friend have fun!", lambda : self.window_packer(self.SMS_BOMBING_WIN))
		sms.place(x=10,y=260)

		email = extn.OPButtons(self.mainF, "Email Bombing","./media/email.png", "Email bombing..\nSend spand emails to your friend have fun!", lambda : self.window_packer(self.EMAIL_BOMBING_WIN))
		email.place(x=10,y=390)

		#pack the frame
		self.window_packer(self.mainF)

	def window_packer(self, window=None, pack_new = True):
		if not self.PACKED_WINDOWS == []:
			i = self.PACKED_WINDOWS.pop()
			i.pack_forget()
		if pack_new:
			window.pack(fill="both", expand=1)
			self.PACKED_WINDOWS.append(window)
	def go_back_to_home(self):
		self.window_packer(pack_new=False)
		self.UI()


	def get_version(self):
		try:
			return open("./data/.version", "r").read().strip()
		except Exception:
			return '1.0'

#run
if __name__ == "__main__":
	Application = MmainWindow()
	Application.mainloop()
