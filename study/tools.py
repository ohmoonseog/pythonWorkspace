from typing import Text
import clipboard
import base64
import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES
import tkinter as tk
import tkinter.ttk as ttk
from tkscrolledframe import ScrolledFrame
from pygubu.widgets.tkscrolledframe import TkScrolledFrame
from tkinter.scrolledtext import ScrolledText

class sqlLiteExecute:
    def __init__(self,dbFilePath):
        import sqlite3
        self.conn = sqlite3.connect(dbFilePath)
        self.cur = self.conn.cursor()
    def callSql(self,sql,parameters = None):
        if parameters == None:
            self.cur.execute(sql)
        else :
            self.cur.execute(sql,parameters)
        return self.cur.fetchall()
    def close(self):
        self.conn.close()


class  MyCipher:
    def __init__( self,keyNum ):
        self.BS = 16
        self.pad = lambda s: s + ( self.BS- len(s.encode('utf-8')) % self.BS) * chr(self.BS - len(s.encode('utf-8')) % self.BS)
        self.unpad = lambda s : s[0:-s[-1]]
        self.key = hashlib.sha256(keyNum.encode('utf-8')).digest()
       
    def encrypt( self, raw ):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new( self.key, AES.MODE_CFB, iv)
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf-8') ))

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new( self.key, AES.MODE_CFB, iv )
        return self.unpad(cipher.decrypt(enc[16:] ))

    def encrypt_str( self, raw ):
        return self.encrypt(raw).decode('utf-8')

    def decrypt_str( self, enc ):
        if type(enc) == str:
            enc = str.encode(enc)
        return self.decrypt(enc).decode('utf-8')
        
class ToolsApp:
    def __init__(self, master=None):
        # build ui
        iBPadx = 10
        iBPadY = 3        
        self.frameMain = tk.Frame(master)
        self.frameMain.configure(height='550', width='440',bd=1,highlightthickness=1)
        self.frameMain.pack(expand='true', fill='both', side='top')
        self.frameSub1 = tk.Frame(self.frameMain)
        self.frameSub2 = tk.Frame(self.frameMain)
        self.frameSub3 = tk.Frame(self.frameMain)
        self.frameSub1.configure(borderwidth='1', height='20', highlightthickness='1', padx='5',pady='5', width='200')
        self.frameSub2.configure(borderwidth='1', height='200', highlightthickness='1', width='200')
        self.frameSub3.configure(width='200',height='220', padx='5', pady='5')
        self.frameSub1.grid(column='0', row='0', sticky='ne')
        self.frameSub3.grid(column='1', row='0', rowspan='2', sticky='news')
        self.frameSub2.grid(column='0', row='1', sticky='es')
        self.frameSub3.grid_propagate(0)

        self.label_1 = tk.Label(self.frameSub1)
        self.label_1.configure(text='CMD')
        self.label_1.pack(side='left')
        self.entry_1 = tk.Entry(self.frameSub1)
        self.entry_1.delete('0', 'end')
        self.entry_1.insert('0', "http://www.daum.net")
        self.entry_1.pack(side='left')
        self.btnCall = tk.Button(self.frameSub1)
        self.btnCall.configure(cursor='arrow', text='CALL')
        self.btnCall.pack(side='right')
        self.tkscrolledframe_2 = TkScrolledFrame(self.frameSub2, scrolltype='both')
        self.buttonItem = []
        idx = 0
        buttonWidth = 33
        sqllite = sqlLiteExecute('tools.db')
        rowLite = sqllite.callSql("select gbn ,ord,name,data,reg_date from tb_tools order by ord")
        for row in rowLite:
            self.buttonItem.append ( tk.Button(self.tkscrolledframe_2,text=row[2],command=lambda text = row[3],gbn = row[0] : self.fnClipboardCopy(gbn,text),bd=1,highlightthickness=1))
            self.buttonItem[idx].pack(pady=iBPadY,padx=iBPadx)
            self.buttonItem[idx].config(width=buttonWidth)
            idx += 1
        sqllite.close()
        self.buttonQuit = tk.Button(self.tkscrolledframe_2,text="QUIT",command=master.destroy,bd=1,highlightthickness=1)
        self.buttonQuit.pack(side = tk.BOTTOM,pady=iBPadY,padx=iBPadx)
        self.buttonQuit.config(width=buttonWidth)
        self.buttonNojs = tk.Button(self.tkscrolledframe_2,text="NOJS",bd=1,highlightthickness=1)
        self.buttonNojs.bind("<Button-1>",self.fnCopy)
        self.buttonNojs.pack(side = tk.BOTTOM,pady=iBPadY,padx=iBPadx)
        self.buttonNojs.config(width=buttonWidth)

        self.tkscrolledframe_2.configure(usemousewheel=False)
        self.tkscrolledframe_2.pack(side='top')
        self.tkinterscrolledtext_1 = ScrolledText(self.frameSub3)
        self.tkinterscrolledtext_1.configure(height='17', undo='true', width='25')
        _text_ = ''' ... '''
        self.tkinterscrolledtext_1.insert('0.0', _text_)
        self.tkinterscrolledtext_1.pack(side='top')
        # Main widget
        self.mainwindow = self.frameMain
    def callWebB(self):
        url = self.entry_1.get()
        import webbrowser as wb
        wb.open(url)
    def callRun(self):
        pgm = self.entry_1.get()
        path = pgm[:pgm.rindex("\\")]
        import subprocess as sb
        sb.Popen(pgm,cwd=path) 
    def fnClipboardCopy(self,gbn,text):
        if gbn == "URL":
            import webbrowser as wb
            wb.open(text)
        elif gbn == "RUN":
            path = text[:text.rindex("\\")]
            import subprocess as sb
            sb.Popen(text,cwd=path) 
        clipboard.copy(self.getPassword(text))
    def fnCopy(self,event):
        text = "javascript:function r(d){d.oncontextmenu=null;d.onselectstart=null;d.ondragstart=null;d.onkeydown=null;d.onmousedown=null;}function unify(w){try{r(w.document);}catch(e){}try{r(w.document.body);}catch(e){}try{var divs=w.document.getElementsByTagName('div');for(var i=0;i<divs.length;i++){try{r(divs[i]);}catch(e){}}}catch(e){}for(var i=0;i<w.frames.length;i++){try{unify(w.frames[i].window);}catch(e){}}}unify(self);"
        clipboard.copy(text)
    def getPassword(self,pwd=""):
        key = self.entry_1.get()
        pwd
        text = pwd
#        text = MyCipher(key).decrypt(pwd)        
#        text = MyCipher(key).encrypt(pwd)
        self.entry_1.delete(0,tk.END)
        self.entry_1.insert(0,text)
        return text

    def run(self):
        self.mainwindow.mainloop()

class app(tk.Tk):
    def __init__(self, **args):
        iBPadx = 10
        iBPadY = 3
        super().__init__(**args)
        self.geometry('310x550')
        self.title("GO TO")
        self.frameMain = tk.Frame(master=self,bd=1,highlightthickness=1)
        self.frameMain.configure(height='200', width='200')
        self.frameMain.pack(expand='true', fill='both', side='top')        
        self.frameSub1 = tk.Frame(master=self.frameMain, width=100, height=50,bd=1,highlightthickness=1)
        self.frameSub1.grid(sticky='nw')
        self.frameSub2 = tk.Frame(master=self.frameMain, width=100, height=250,bd=1,highlightthickness=1)
        self.frameSub2.configure(borderwidth='1', height='200', highlightthickness='1', width='200')
        self.frameSub2.grid(column='0', row='1', sticky='w')

        self.frameSub3 = tk.Frame(self.frameMain)
        self.frameSub3.configure(height='240', padx='5', pady='5', relief='raised')
        self.frameSub3.configure(width='200')
        self.frameSub3.grid(column='1', row='0', rowspan='2', sticky='e')
        self.frameSub3.grid_propagate(0)


        self.lable1 = tk.Label(master=self.frameSub1)
        self.lable1.grid(row=0,column=0,pady=iBPadY,padx=iBPadx)
        self.lable1.config(text="CMD",highlightthickness=1)
        self.entry1 = tk.Entry(master=self.frameSub1) 
        self.entry1.focus_set()
        self.entry1.insert(0,"http://www.daum.net")
        self.entry1.config(bd=1,highlightthickness=1)
        self.entry1.grid(row=0,column=1,pady=iBPadY,padx=iBPadx)
        self.buttonCall = tk.Button(master=self.frameSub1,text="Call",bd=1,highlightthickness=1,command=self.callWebB) 
        self.buttonCall.grid(row=0,column=2,pady=iBPadY)

        self.sf = ScrolledFrame(self.frameSub2, width=640 , )
        self.sf.pack(side="top", expand=1, fill="both")        
        self.sf.bind_arrow_keys(self.frameSub2)
        self.sf.bind_scroll_wheel(self.frameSub2)
        self.inner_frame = self.sf.display_widget(tk.Frame)

        self.buttonItem = []
        idx = 0
        buttonWidth = 33


        sqllite = sqlLiteExecute('tools.db')
        rowLite = sqllite.callSql("select gbn ,ord,name,data,reg_date from tb_tools order by ord")
        for row in rowLite:
            self.buttonItem.append ( tk.Button(self.inner_frame,text=row[2],command=lambda text = row[3],gbn = row[0] : self.fnClipboardCopy(gbn,text),bd=1,highlightthickness=1))
            self.buttonItem[idx].pack(pady=iBPadY,padx=iBPadx)
            self.buttonItem[idx].config(width=buttonWidth)
            idx += 1
        sqllite.close()
        self.buttonQuit = tk.Button(self.inner_frame,text="QUIT",command=self.destroy,bd=1,highlightthickness=1)
        self.buttonQuit.pack(side = tk.BOTTOM,pady=iBPadY,padx=iBPadx)
        self.buttonQuit.config(width=buttonWidth)
        self.buttonNojs = tk.Button(self.inner_frame,text="NOJS",command=self.fnCopy,bd=1,highlightthickness=1)
        self.buttonNojs.pack(side = tk.BOTTOM,pady=iBPadY,padx=iBPadx)
        self.buttonNojs.config(width=buttonWidth)
        self.tkinterscrolledtext_1 = ScrolledText(self.frameSub3)
        self.tkinterscrolledtext_1.configure(height='17', undo='true', width='25')
        _text_ = '''text'''
        self.tkinterscrolledtext_1.insert('0.0', _text_)
        self.tkinterscrolledtext_1.pack(side='top')

    def callWebB(self):
        url = self.entry1.get()
        import webbrowser as wb
        wb.open(url)
    def callRun(self):
        pgm = self.entry1.get()
        path = pgm[:pgm.rindex("\\")]
        import subprocess as sb
        sb.Popen(pgm,cwd=path) 
    def fnClipboardCopy(self,gbn,text):
        if gbn == "URL":
            import webbrowser as wb
            wb.open(text)
        elif gbn == "RUN":
            path = text[:text.rindex("\\")]
            import subprocess as sb
            sb.Popen(text,cwd=path) 
        clipboard.copy(self.getPassword(text))
    def fnCopy(self):
        text = "javascript:function r(d){d.oncontextmenu=null;d.onselectstart=null;d.ondragstart=null;d.onkeydown=null;d.onmousedown=null;}function unify(w){try{r(w.document);}catch(e){}try{r(w.document.body);}catch(e){}try{var divs=w.document.getElementsByTagName('div');for(var i=0;i<divs.length;i++){try{r(divs[i]);}catch(e){}}}catch(e){}for(var i=0;i<w.frames.length;i++){try{unify(w.frames[i].window);}catch(e){}}}unify(self);"
        clipboard.copy(text)
    def getPassword(self,pwd=""):
        key = self.entry1.get()
        pwd
        text = pwd
#        text = MyCipher(key).decrypt(pwd)        
#        text = MyCipher(key).encrypt(pwd)
        self.entry1.delete(0,tk.END)
        self.entry1.insert(0,text)
        return text
if __name__ == '__main__':    
    app().mainloop()
    '''
    root = tk.Tk()
    root.geometry('440x550')
    app = ToolsApp(root)
    app.run()
    '''