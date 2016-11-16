# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
import tkFileDialog
from PIL import Image
from collections import defaultdict
import threading


class Application(Frame):
	
	'''
	Python UI 初始化
	'''
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack(side="top",fill=BOTH, expand=1)
		self.createWidgets()
		self.master.title("Using image averaging to reduce the high ISO noise")

		# 檔案路徑宣告
		self.FilesPath = ()
		self.Images = list() # 將每一章影像的pixel載入的list
		self.ImagesSizeList = list() # 取得每張圖片的大小
		self.OutputImage = None

	'''
	取得檔案路徑
	'''
	def GetImagesPath(self):
		# 限制能載入的副檔名
		self.dir_opt = {}
		self.dir_opt['filetypes'] = [('PNG', '.png'), ('JPEG', ('.jpg','.jpeg','.jpe','.jfif')),(u'點陣圖',('.bmp','.dib'))]
		FilesPath = tkFileDialog.askopenfilenames(parent=self,title='Choose a file',**self.dir_opt)

		if len(FilesPath)>0 :
			self.FilesPath += FilesPath
			self.EditListLabel(self.FilesPath)
			self.EditStateLabel("影像路徑載入完成")

	'''
	編輯[輸入路徑Label]的顯示內容
	'''
	def EditListLabel(self,FilesPath):
		self.InputLabel['text'] = "Image Path:\n"
		for Path in FilesPath:
			self.InputLabel['text'] += "\t"+Path+"\n"

	'''
	清除[輸入路徑Label]的內容及檔案路徑的變數
	'''
	def ClearListLabel(self):
		self.EditStateLabel("清除完成      ")
		self.FilesPath = ()
		self.InputLabel['text'] = "Image Path:\n"

	'''
	編輯[狀態Label]的顯示內容
	'''
	def EditStateLabel(self,inptext=""):
		self.State['text'] = "State: "+ inptext
		self.State.pack()

	'''
	載入影像
	'''
	def ReadImageFile(self):
		if len(self.FilesPath) > 0:
			# 將每一章影像的pixel載入的list
			self.Images = list() 
			# 取得每張圖片的大小
			self.ImagesSizeList = list() 

			for ImagePath in self.FilesPath:
				imtemp = Image.open(ImagePath)
				self.Images.append(imtemp.load())
				self.ImagesSizeList.append(imtemp.size)
			return True
		else:
			return False

	'''
	檢查所有圖片大小是否一致
	'''
	def CheckImageSize(self):
		count = defaultdict(int)
		for ImagesSize in self.ImagesSizeList:
			count[ImagesSize]+=1
		if len(count) == 1:
			return True
		else:
			return False

	'''
	降低高斯雜訊
	'''
	def ReduceNoise(self):
		self.OutputImage = Image.new("RGB", self.ImagesSizeList[0])
		ix,iy = self.ImagesSizeList[0]
		ImagesNum = len(self.Images)
		for x in xrange(ix):
			for y in xrange(iy):
				R,G,B = 0,0,0 
				for im in self.Images:
					r,g,b = im[x,y]
					R+=r
					G+=g
					B+=b
				R = int(R/ImagesNum)
				G = int(G/ImagesNum)
				B = int(B/ImagesNum)
				self.OutputImage.putpixel((x,y),(R,G,B))

	'''
	Start按鈕點擊事件
	'''
	def StartFunction(self):
		self.Start['state']='disable'
		self.EditStateLabel("影像處理中...        ")	
		threading.Thread(target = self.StartThread).start()

	'''
	此function為Start按鈕所需的Thread Function
	'''
	def StartThread(self):
		if self.ReadImageFile():
			if self.CheckImageSize():
				self.ReduceNoise()
				self.EditStateLabel("影像處理完畢")
				self.OutputImage.show()
			else:
				self.EditStateLabel("輸入影像大小不一致")

		else:
			self.EditStateLabel("未輸入影像，請案Load按鈕輸入影像")
		self.Start['state']='normal'

	'''
	Save按鈕點擊事件
	'''
	def SaveFucntion(self):
		self.EditStateLabel("圖片儲存中")
		self.Save['state']='disable'
		threading.Thread(target = self.SaveThread).start()

	'''
	此function為Save按鈕所需的Thread Function
	'''
	def SaveThread(self):
		if self.OutputImage is not None:
			SaveFileName = tkFileDialog.asksaveasfile(defaultextension=".jpg")
			if SaveFileName is None:
				self.Save['state']='normal'
				return
			self.OutputImage.save(SaveFileName)
			self.EditStateLabel("圖片儲存完成")
		else:
			self.EditStateLabel("無法輸出圖片")
		self.Save['state']='normal'

	'''
	Quit按鈕點擊事件 - 離開程式
	'''
	def QuitWindow(self):
		self.quit()

	'''
	設定介面與按鈕
	'''
	def createWidgets(self):
		self.ButtonFrame = Frame(self)
		self.ButtonFrame.pack()

		self.Load = Button(self.ButtonFrame,text="Load",command=self.GetImagesPath)
		self.Load.pack(side="left", expand=1)

		self.Clear = Button(self.ButtonFrame,text="Clear",command=self.ClearListLabel)
		self.Clear.pack(side="left", expand=1)

		self.Start = Button(self.ButtonFrame,text="Start",command=self.StartFunction)
		self.Start.pack(side="left", expand=1)

		self.Save = Button(self.ButtonFrame,text="Save",command=self.SaveFucntion)
		self.Save.pack(side="left", expand=1)

		self.Quit = Button(self.ButtonFrame,text="Quit",command=self.QuitWindow)
		self.Quit.pack(side="left", expand=1)

		self.State = Label(self, text="State: ")
		self.State.pack(anchor=W, padx=5, pady=5)

		self.InputLabel = Label(self, text="Image Path:\n")
		self.InputLabel.pack(anchor=W, padx=5, pady=5)

def main():
	root = Tk()
	# 設定視窗大小
	root.geometry("650x300+300+300")
	# 禁止調整視窗大小
	root.resizable(False, False)
	app = Application(master=root)
	app.mainloop()
		
if __name__ == '__main__':
	main()