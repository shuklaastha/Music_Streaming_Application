import matplotlib.pyplot as plt
from model import *

def bar_graph():
    r1 = Song.query.filter(Song.rating.between(0.0,1.0)).all()
    r2 = Song.query.filter(Song.rating.between(1.0,2.0)).all()
    r3 = Song.query.filter(Song.rating.between(2.0,3.0)).all()
    r4 = Song.query.filter(Song.rating.between(3.0,4.0)).all()
    r5 = Song.query.filter(Song.rating.between(4.0,5.0)).all()
       
    d = {'0.0-1.0': 0, '1.0-2.0': 0, '2.0-3.0': 0, '3.0-4.0': 0}
    d['0.0-1.0']=len(r1)
    d['1.0-2.0']=len(r2)
    d['2.0-3.0']=len(r3)
    d['3.0-4.0']=len(r4)
    d['4.0-5.0']=len(r5)
    labels=d.keys()
    values=d.values()
    plt.bar(labels, values, color='blue')
    plt.xlabel('Ratings')
    plt.ylabel('No. of songs')
    plt.title('Bar Graph')
    plt.savefig('C:/Users/Astha/MAD1 Project 22f1000725/static/BarGraph.jpeg')
    plt.clf()



def pie_chart():
    c= User.query.filter_by(creator="yes").all()
    creator_count=len(c)
    print(creator_count)
    u = User.query.all()
    x=len(u)-creator_count
    user_count =x
    print(user_count)
    
    data ={"TOTAL USERS":0, "CREATORS":0 , "USERS NOT CREATORS":0}
    data["TOTAL USERS"]=user_count+creator_count
    data["CREATORS"]=creator_count
    data["USERS NOT CREATORS"]=user_count
    print(data["TOTAL USERS"])
    labels=data.keys()
    sizes=data.values()
        
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  
    plt.title("piechart")
    plt.savefig('C:/Users/Astha/MAD1 Project 22f1000725/static/PieChart.jpeg')
    plt.clf()


