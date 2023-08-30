import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

class linear:
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Intervels")
        self.root.geometry(f"500x500+{(self.root.winfo_screenwidth()//2)-(500//2)}+{(self.root.winfo_screenheight()//2)-(500//2)}")
        
        select_button = tk.Button(self.root, text = "Select File", command = self.select_file)
        select_button.place(x = 100, y = 10)
        
        self.file_entry = tk.Entry(self.root)
        self.file_entry.place(x = 200, y = 10)
        
        show_button = tk.Button(self.root,text="show",command=self.show)
        show_button.place(x = 100, y = 70)
        
        quit_button = tk.Button(self.root,text='Quit',command=self.root.destroy)
        quit_button.place(x = 450, y = 450)
    
    
    def select_file(self):
        
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(tk.END, self.file_path)
    
    
    
    def show(self):
        
        self.data = pd.read_excel(self.file_path)
        
        self.int_time = list(self.data.iloc[:,0].values)
        self.int_ffr  = list(self.data.iloc[:,1].values)
        self.int_cofr = list(self.data.iloc[:,2].values)
        self.int_ffc  = list(self.data.iloc[:,3].values)
        self.int_cofc = list(self.data.iloc[:,4].values)
        self.int_wear = list(self.data.iloc[:,5].values)

        self.n = len(self.int_time)
        
        
        def compute(y):
            
            sum_time,sum_ffr = self.int_time[0],y[0]
            sum_timeffr = self.int_time[0]*y[0]
            sum_sqtime = self.int_time[0]**2
            
            store = []
            
            i,j,r,temp = 0,1,0,0
            
            while j!=self.n:
                
                sum_time = sum_time + self.int_time[j]
                sum_ffr  = sum_ffr  + y[j]
                sum_timeffr = sum_timeffr + self.int_time[j]*y[j]
                sum_sqtime = sum_sqtime + self.int_time[j]**2
                
                length = j-i+1
                m = ((length*sum_timeffr) - (sum_time*sum_ffr))/((length*sum_sqtime)-(sum_time)**2)
                c = ((sum_ffr)-(m*sum_time))/length
                print(m,c)
                
                rss = 0
                tss = 0
                
                for k in range(length):
                    rss = rss + (y[i+k] - (m*self.int_time[i+k]+c))**2
                    tss = tss + (y[i+k] - (sum_ffr/length))**2
                    
                # temp = r
                r = 1-(rss/tss)
                
                
                if r>0.95:
                    j = j + 1
                    if j >= self.n:
                        store.append([i,j-1,m,c])
                        # print(i,j-1,m,c,temp)
                        break
                else:
                    store.append([i,j-1,m,c])
                    # print(i,j,m,c,temp)
                    # if i==j:
                    #     i = j + 1
                    # else:
                    #     i = j
                    i = j - 1
                    sum_time = self.int_time[i]
                    sum_ffr  = y[i]
                    sum_timeffr = self.int_time[i]*y[i]
                    sum_sqtime  = self.int_time[i]**2
                    if j >= self.n:
                        store.append([i,j-1,m,c])
                        # print(i,j-1,m,c,temp)
                        break
            
            return store
        
        
        self.r_ffr = compute(self.int_ffr)
        self.r_cofr = compute(self.int_cofr)
        self.r_wear = compute(self.int_wear)
        print(self.r_ffr)
        print(self.r_cofr)
        print(self.r_wear)

        graph1 = tk.Button(self.root,text="Time vs Cofr",command=self.graph1)
        graph1.place(x = 150, y = 110)
        
        graph2 = tk.Button(self.root,text="Time vs ffr",command=self.graph2)
        graph2.place(x = 150, y = 150)
        
        graph5 = tk.Button(self.root,text="Time vs wear",command=self.graph3)
        graph5.place(x = 150, y = 190)
    
    
    
    def plot(self, r_list):
        
        fig, (old,new) = plt.subplots(2)
        old.set_title('Time VS ffr (Given data)')
        old.plot(self.int_time, self.int_ffr)
        new.set_title(f'Time VS ffr (Linear)')
        
        
        for i in r_list:
            
            x = self.int_time[i[0]:i[1]+1]
            m = i[2]
            c = i[3]
            y = []
            
            for j in x:
                
                y.append(m*j+c)
                
            plt.plot(x,y)
        
        plt.tight_layout()
        plt.show()
    
    
    def graph1(self):
        self.plot(self.r_ffr)
    
    
    def graph2(self):
        self.plot(self.cofr)
    
    def graph3(self):
        self.plot(self.wear)
    
    
    def run(self):
        self.root.mainloop()

a = linear()
a.run()