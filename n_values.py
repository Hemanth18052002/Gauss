import tkinter as tk
from tkinter import filedialog
import pandas as pd
from scipy.interpolate import make_interp_spline

class nvalue:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Intervels")
        self.root.geometry(f"500x500+{(self.root.winfo_screenwidth()//2)-(500//2)}+{(self.root.winfo_screenheight()//2)-(500//2)}")
        
        select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        select_button.place(x=100,y = 10)
        
        self.file_entry = tk.Entry(self.root)
        self.file_entry.place(x=200,y = 10)
        
        label_n = tk.Label(self.root, text="Enter the size of interval")
        label_n.place(x = 100, y = 40)
        
        self.nvalue = tk.Entry(self.root)
        self.nvalue.place(x=200, y=40)
        
        show_button = tk.Button(self.root,text="show",command=self.show)
        show_button.place(x=100, y=70)
        
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(tk.END, self.file_path)
    
    
    def run(self):
        self.root.mainloop()


    def show(self):
        self.data = pd.read_excel(self.file_path)
        int_time = list(self.data.iloc[:,0:1].values)
        int_ffr  = list(self.data.iloc[:,1].values)
        int_cofr = list(self.data.iloc[:,2].values)
        int_ffc  = list(self.data.iloc[:,3].values)
        int_cofc = list(self.data.iloc[:,4].values)


        dic = {}
        for i in range(len(int_time)):
            k = int(int_time[i])
            try:
                dic[k].append(int_time[i])
            except:
                dic[k]=[]
                dic[k].insert(0,int_time[i])
                
                
        c,inde,p = 0,0,0

        res_ffr,res_cofr,res_ffc,res_cofc = [],[],[],[]
        nvalue = int(self.nvalue.get())
        
        for i in range(len(int_time)-1):
            
            c = c + nvalue
            try:
                dic_int_time = dic[c-1]+dic[c]
                dic_int_time = ([k[0] for k in dic_int_time])
                
                while p!=c-1:
                    inde = inde + len(dic[p])
                    p = p + 1
                p = c + 1
                
                
                # ffr
                dic_int_ffr = int_ffr[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_ffr, k=len(dic_int_time)-1)
                res_ffr.append(X_Y_Spline([float(c)]))
                
                #cofr
                dic_int_cofr = int_cofr[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_cofr, k=len(dic_int_time)-1)
                res_cofr.append(X_Y_Spline([float(c)]))
                
                #ffc
                dic_int_ffc = int_ffc[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_ffc, k=len(dic_int_time)-1)
                res_ffc.append(X_Y_Spline([float(c)]))
                
                #cofc
                dic_int_cofc = int_cofc[inde:inde+len(dic_int_time)]
                X_Y_Spline = make_interp_spline(dic_int_time, dic_int_cofc, k=len(dic_int_time)-1)
                res_cofc.append(X_Y_Spline([float(c)]))
                
            except:
                pass
            try:
                inde = inde + len(dic[c-1]) + len(dic[c])
            except:
                # break
                pass
            
            

        res_ffr  = ([k[0] for k in res_ffr])
        res_cofr = ([k[0] for k in res_cofr])
        res_ffc  = ([k[0] for k in res_ffc])
        res_cofc = ([k[0] for k in res_cofc])

        xt = list(float(i) for i in range(nvalue,len(res_ffr)+1,nvalue))


        res = {}
        fin_time,fin_ffr,fin_cofr,fin_ffc,fin_cofc = {},{},{},{},{}


        for i in range(len(xt)):
            fin_time[i] = xt[i]
            fin_ffr[i] = res_ffr[i]
            fin_cofr[i] = res_cofr[i]
            fin_ffc[i] = res_ffc[i]
            fin_cofc[i] = res_cofc[i]
            
        res['Time(sec)'] = fin_time
        res['ffr(N)']    = fin_ffr
        res['cofr']      = fin_cofr
        res['ffc(N)']    = fin_ffc
        res['cofc']      = fin_cofc
            
        run1 = pd.DataFrame(res)
        print(run1)

a = nvalue()
a.run()