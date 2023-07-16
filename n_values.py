import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime as dt
from scipy.interpolate import make_interp_spline

class nvalue:
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Intervels")
        self.root.geometry(f"500x500+{(self.root.winfo_screenwidth()//2)-(500//2)}+{(self.root.winfo_screenheight()//2)-(500//2)}")
        
        select_button = tk.Button(self.root, text = "Select File", command = self.select_file)
        select_button.place(x = 100, y = 10)
        
        self.file_entry = tk.Entry(self.root)
        self.file_entry.place(x = 200, y = 10)
        
        label_n = tk.Label(self.root, text="Enter the size of interval")
        label_n.place(x = 100, y = 40)
        
        self.nvalue = tk.Entry(self.root)
        self.nvalue.place(x = 200, y = 40)
        
        show_button = tk.Button(self.root,text="show",command=self.show)
        show_button.place(x = 100, y = 70)
        
        graph1 = tk.Button(self.root, text='Time VS ffr',command = self.graph1)
        graph1.place(x = 150, y = 110)
        
        graph2 = tk.Button(self.root, text='Time VS cofr', command = self.graph2)
        graph2.place(x = 150, y = 150)
        
        graph3 = tk.Button(self.root, text='Time VS ffc', command = self.graph3)
        graph3.place(x = 150, y = 190)
        
        graph4 = tk.Button(self.root, text='Time VS cofc', command = self.graph4)
        graph4.place(x = 150, y = 230)
        
        graph5 = tk.Button(self.root, text = 'Time VS wear', command = self.graph5)
        graph5.place(x = 150, y = 270)
        

        quit_button = tk.Button(self.root,text='Quit',command=self.root.destroy)
        quit_button.place(x = 450, y = 450)



    def select_file(self):
        
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(tk.END, self.file_path)



    def show(self):
        
        self.data = pd.read_excel(self.file_path)
        
        self.int_time = list(self.data.iloc[:,0:1].values)
        self.int_ffr  = list(self.data.iloc[:,1].values)
        self.int_cofr = list(self.data.iloc[:,2].values)
        self.int_ffc  = list(self.data.iloc[:,3].values)
        self.int_cofc = list(self.data.iloc[:,4].values)
        self.int_wear = list(self.data.iloc[:,5].values)


        dic = {}
        
        for i in range(len(self.int_time)):
            
            k = int(self.int_time[i])
            
            try:
                
                dic[k].append(self.int_time[i])
                
            except:
                
                dic[k]=[]
                dic[k].insert(0,self.int_time[i])
                
                
                
        c,inde,p = 0,0,0

        self.res_ffr,self.res_cofr,self.res_ffc,self.res_cofc,self.res_wear = [],[],[],[],[]
        nvalue = int(self.nvalue.get())
        
        
        for i in range(len(dic)-1):
            
            c = c + nvalue
            
            try:
                
                dic_int_time = dic[c-1]+dic[c]
                dic_int_time = ([k[0] for k in dic_int_time])
                
                while p!=c-1:
                    
                    inde = inde + len(dic[p])
                    p = p + 1
                    
                p = c + 1
                
                
                # ffr
                dic_int_ffr = self.int_ffr[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_ffr, k=len(dic_int_time)-1)
                self.res_ffr.append(X_Y_Spline([float(c)]))
                
                #cofr
                dic_int_cofr = self.int_cofr[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_cofr, k=len(dic_int_time)-1)
                self.res_cofr.append(X_Y_Spline([float(c)]))
                
                #ffc
                dic_int_ffc = self.int_ffc[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_ffc, k=len(dic_int_time)-1)
                self.res_ffc.append(X_Y_Spline([float(c)]))
                
                #cofc
                dic_int_cofc = self.int_cofc[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_cofc, k=len(dic_int_time)-1)
                self.res_cofc.append(X_Y_Spline([float(c)]))
                
                #wear
                dic_int_wear = self.int_wear[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_wear, k=len(dic_int_time)-1)
                self.res_wear.append(X_Y_Spline([float(c)]))

            except:
                pass
            
            
            try:
                inde = inde + len(dic[c-1]) + len(dic[c])
            except:
                pass
            
            

        self.res_ffr  = ([k[0] for k in self.res_ffr])
        self.res_cofr = ([k[0] for k in self.res_cofr])
        self.res_ffc  = ([k[0] for k in self.res_ffc])
        self.res_cofc = ([k[0] for k in self.res_cofc])
        self.res_wear = ([k[0] for k in self.res_wear])

        self.xt = []
        k = nvalue
        
        while k<self.int_time[-1][0]:
            
            self.xt.append(float(k))
            k = k + nvalue

        # print(self.xt)
        
        res = {}
        fin_time,fin_ffr,fin_cofr,fin_ffc,fin_cofc,fin_wear = {},{},{},{},{},{}


        for i in range(len(self.xt)):
            
            fin_time[i] = self.xt[i]
            fin_ffr[i]  = self.res_ffr[i]
            fin_cofr[i] = self.res_cofr[i]
            fin_ffc[i]  = self.res_ffc[i]
            fin_cofc[i] = self.res_cofc[i]
            fin_wear[i] = self.res_wear[i]
        
        
        res['Time(sec)'] = fin_time
        res['ffr(N)']    = fin_ffr
        res['cofr']      = fin_cofr
        res['ffc(N)']    = fin_ffc
        res['cofc']      = fin_cofc
        res['wear(um)']  = fin_wear
        
        
        excel_name = str(list(self.file_path.split('/'))[-1])[:-5] + f'_result_sizeof_{nvalue}_'
        now = dt.now()
        excel_name = excel_name + str(now.strftime('%d_%m_%Y_at_%H_%M_%S')) + '.xlsx'
        
        download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        download_path = os.path.join(download_folder, excel_name)
        
        result = pd.DataFrame(res)
        # print(result)
        result.to_excel(download_path)
        
        # print("Downloaded at ",download_path)
        
        os.startfile(download_path)

    def graph1(self):
        fig, (old,new) = plt.subplots(2)
        
        old.set_title('Given data (Time VS ffr)')
        old.plot(self.int_time, self.int_ffr)
        
        new.set_title('Intervaled data (Time VS ffr)')
        new.plot(self.xt, self.res_ffr)
        
        plt.tight_layout()
        
        plt.show()
    
    def graph2(self):
        fig, (old,new) = plt.subplots(2)
        
        old.set_title('Given data (Time VS cofr)')
        old.plot(self.int_time, self.int_cofr)
        
        new.set_title('Intervaled data (Time VS cofr)')
        new.plot(self.xt, self.res_cofr)
        
        plt.tight_layout()
        
        plt.show()
    
    def graph3(self):
        fig, (old,new) = plt.subplots(2)
        
        old.set_title('Given data (Time VS ffc)')
        old.plot(self.int_time, self.int_ffc)
        
        new.set_title('Intervaled data (Time VS ffc)')
        new.plot(self.xt, self.res_ffc)
        
        plt.tight_layout()
        
        plt.show()
    
    
    def graph4(self):
        fig, (old,new) = plt.subplots(2)
        
        old.set_title('Given data (Time VS cofc)')
        old.plot(self.int_time, self.int_cofc)
        
        new.set_title('Intervaled data (Time VS cofc)')
        new.plot(self.xt, self.res_cofc)
        
        plt.tight_layout()
        
        plt.show()
        

    def graph5(self):
        fig, (old,new) = plt.subplots(2)
        
        old.set_title('Given data (Time VS wear)')
        old.plot(self.int_time, self.int_wear)
        
        new.set_title('Intervaled data (Time VS wear)')
        new.plot(self.xt, self.res_wear)
        
        plt.tight_layout()
        
        plt.show()
    
    def run(self):
        self.root.mainloop()

a = nvalue()
a.run()
