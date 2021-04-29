import requests, smtplib, random
from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL
from email.message import EmailMessage
app=Flask(__name__)
app.secret_key='man'
app.config['MYSQL_USER'] = 'sql12386740'
app.config['MYSQL_PASSWORD'] = 'AwXfZAmnQu'
app.config['MYSQL_DB'] = 'sql12386740'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)

@app.route('/con',methods=['POST','GET']) 
def con():
    if request.method=='POST':
        l=[]
        if request.form.get("se"):
                d = request.form['ser']
                d=d.lower()
                cur=mysql.connection.cursor()
                cur.execute("select * from stock")
                mysql.connection.commit()
                r=cur.fetchall()
                for i in r:
                    l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                    p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                    for q in l1:
                        if q not in p:
                            l1=l1+q
                    o=l1.lower()
                    for j in d.split(' '):
                        if j in o:
                            l.append(i)
                            break
                session['s']=l
                session['p']=len(session['s'])
                return redirect("/s")
        if request.form.get("sub"):
            """
            toaddr  = request.form['txtEmail']
            passwor = "bbb@54321"
            msg = EmailMessage()
            msgt='Thank you for connecting with us.\nBrilliants Books'
            msg.set_content(msgt)
            msg['Subject'] = "Thanks From Brilliant Books"
            msg['From'] = 'Brilliant Books'
            msg['To'] = toaddr
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("brilliantbooks0@gmail.com", passwor)
            server.send_message(msg)
            server.quit()
            toaddrs  = "brilliantbooks0@gmail.com"
            password = "bbb@54321"
            msg = EmailMessage()
            msgtxt='From '+request.form['txtName']+'\n'+request.form['txtMsg']+'\n'+'Contact: '+request.form['txtPhone']+'\n'+request.form['txtEmail']
            msg.set_content(msgtxt)
            msg['Subject'] = "From contact us"
            msg['From'] = 'Brilliant Books'
            msg['To'] = toaddrs
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("brilliantbooks0@gmail.com", password)
            server.send_message(msg)
            server.quit()
            """
            flash("Thank you for connecting with us")
            return redirect('/con')
    else:
        return render_template("contact.html")
    
@app.errorhandler(404) 
def not_found(e):
    if 'det' not in session:
        session['det'] = []
    d=request.url
    na=''
    for i in d[::-1]:
        na=na+i
        if i=='/':
            break
    num=na[::-1]
    cur=mysql.connection.cursor()
    cur.execute("select * from stock where ISBN like %s",(num[1:],))
    mysql.connection.commit()
    r=cur.fetchall()
    rrm=list(r)
    cur.execute("select * from stock where Rec like 'Yes'")
    mysql.connection.commit()
    t=cur.fetchall()
    tm=list(t)[::-1]
    l=[]
    if len(r)==0:
        return redirect("/")
    if request.method=='POST':
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            rm=cur.fetchall()
            for i in r:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
        
        if request.form.get("cart"):
            q = request.form['qua']
            det = session['det']
            det.append([rrm[0]]*int(q))
            session['det'] = det
            return redirect("/"+num[1:])
        
        if request.form.get("buy"):
            q = request.form['qua']
            det = session['det']
            det.append([rrm[0]]*int(q))
            session['det'] = det
            return redirect("/buynow")
    else:
        return render_template("res.html",r=r,tm=tm)
  
@app.route('/',methods=['POST','GET'])
def index():
    l=[]
    cur=mysql.connection.cursor()
    cur.execute("select * from stock where Rec like 'Yes'")
    mysql.connection.commit()
    r=cur.fetchall()
    rm=list(r)[::-1]
    if request.method=='POST':
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            r=cur.fetchall()
            for i in r:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
    else:
        return render_template('home.html',rm=rm)

@app.route('/s',methods=['POST','GET'])
def ser():
    l=[]
    flash("Your Results : ")
    if request.method=='POST':
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            r=cur.fetchall()
            for i in r:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
    else:
        return render_template('search.html')
    
    
@app.route('/adlogin',methods=['POST','GET'])
def log():
    session.pop('ho',None)
    if request.method=='POST':
        if request.form.get("ln"):
            unam = request.form['unam']
            pas = request.form['pas']
            cur=mysql.connection.cursor()
            cur.execute("select * from user where unam like %s",(unam,))
            mysql.connection.commit()
            r=cur.fetchall()
            if unam=='admin' and pas=='bbb54321':
                session['k']=1
                session['ho']='home'
                return redirect("/ahom")
            else:
                session['k']=0
            if len(r)!=0:               
                if unam==r[0]['unam'] and pas==r[0]['pass']:
                    session['ho']='home'
                    return redirect("/ahom")
                else:
                    flash("Wrong Passwords")
                    return redirect("/adlogin")
            else:
                flash("Wrong Username")
                return redirect("/adlogin")
    else:
        return render_template('login.html')

@app.route('/ahom',methods=['POST','GET'])
def ahom():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from user")
        mysql.connection.commit()
        r=cur.fetchall()
        return render_template("adminhome.html",r=r)
    else:
        return redirect('/adlogin')

@app.route('/addsub',methods=['POST','GET'])
def sinup():
    if 'ho' in session:
        if request.method=='POST':
            us = request.form['emal']            
            cur=mysql.connection.cursor()
            cur.execute("select * from user where unam like %s",(us,))
            mysql.connection.commit()
            r=cur.fetchall()
            if len(r)>0:
                flash("Email already exist")
                return redirect('/addsub')
            else:
                fnam = request.form['fnam']
                lnam = request.form['lnam']
                nam=fnam+' '+lnam
                no = request.form['no']
                pp = request.form['pas']
                cpp = request.form['cpas']
                if request.form.get("ln"):
                    return redirect("/ahom")
                if request.form.get("su"):
                    if pp==cpp:
                        cur=mysql.connection.cursor()
                        cur.execute("insert into user values(%s,%s,%s,%s)",(nam,no,us,pp))
                        mysql.connection.commit()
                        return redirect("/ahom")
                    else:
                        flash("Passwords did not match")
                        return redirect("/addsub")
        else:
            return render_template('sinup.html')
    else:
        return redirect("/adlogin")
    
@app.route('/adel',methods=['POST','GET'])
def adel():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from user")
        mysql.connection.commit()
        r=cur.fetchall()
        h=['Name','Number','Username']
        l1=[]
        for i in r:
            l=[i['Name'],i['Number'],i['unam']]
            l1.append(l)
        l1=l1[1:]
        if request.method=='POST':
            if request.form.get("dl"):
                us = request.form['unam']
                cur=mysql.connection.cursor()
                cur.execute("delete from user where unam like %s",(us,))
                mysql.connection.commit()
                flash(f"Successfully deleted {us}")
                return redirect('/adel')
            elif request.form.get("bkk"):
                return redirect('/ahom') 
        else:
            return render_template('Adel.html',h=h,l1=l1)
    else:
        return redirect("/adlogin")
    
    
@app.route('/as',methods=['POST','GET'])
def adds():
    if 'ho' in session:
        if request.method=='POST':
            if request.form.get("bk"):
                return redirect("/ahom")
            if request.form.get("ad"):
                v1 = request.form['bno']
                v2 = request.form['bn']
                v3 = request.form['an']
                v4 = request.form['edi']
                v5 = request.form['pub']
                v6 = request.form['pri']
                v7 = request.form['gen']
                v8 = request.form['qu']
                v9 = request.form['url']
                v10 = request.form['abu']
                v11 = request.form['rec']
                cur=mysql.connection.cursor()
                cur.execute("insert into stock values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11))
                mysql.connection.commit()
                flash(f"Successfully added {v2}")
                return redirect("/as")
        else:
            return render_template('addstock.html')
    else:
        return redirect("/adlogin")
    
@app.route('/rs',methods=['POST','GET'])
def dst():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from stock")
        mysql.connection.commit()
        r=cur.fetchall()
        h=['ISBN', 'Name', 'Author Name', 'Edition', 'Publication', 'Price','Genre','Quantity', 'Image_url','About','Recomendation']
        l1=[]
        for i in r:
            l=[i['ISBN'], i['Name'], i['AName'], i['Edition'], i['Publication'], i['Price'], i['Genre'], i['Quantity'], i['Image_url'],i['About'],i['Rec']]
            l1.append(l)
        if request.method=='POST':
            if request.form.get("dl"):
                us = request.form['unam']
                cur=mysql.connection.cursor()
                cur.execute("select * from stock where ISBN like %s",(us,))
                mysql.connection.commit()
                r=cur.fetchall()
                if len(r)>0:
                    flash(f"Successfully deleted {us} ISBN")
                    cur.execute("delete from stock where ISBN like %s",(us,))
                    mysql.connection.commit()
                    return redirect('/rs')
                elif len(r)==0:
                    flash(f"No record found for ISBN : {us}")
                    return redirect('/rs')
            elif request.form.get("bkk"):
                return redirect('/ahom') 
        else:
            return render_template('dstock.html',h=h,l1=l1)
    else:
        return redirect("/adlogin")
    
    
@app.route('/es',methods=['POST','GET'])
def esk():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from stock")
        mysql.connection.commit()
        r=cur.fetchall()
        h=['ISBN', 'Name', 'Author Name', 'Edition', 'Publication', 'Price','Genre','Quantity', 'Image_url','About','Recomendation']
        l1=[]
        for i in r:
            l=[i['ISBN'], i['Name'], i['AName'], i['Edition'], i['Publication'], i['Price'], i['Genre'], i['Quantity'], i['Image_url'],i['About'],i['Rec']]
            l1.append(l)
        if request.method=='POST':
            if request.form.get("dl"):
                us = request.form['unam']
                fil = request.form['fil']
                val = request.form['val']
                cur=mysql.connection.cursor()
                cur.execute("select * from stock where ISBN like %s",(us,))
                mysql.connection.commit()
                r=cur.fetchall()
                if len(r)>0:
                    flash(f"Successfully edited {us} ISBN")
                    cur.execute(f"update stock set {fil}=%s where ISBN like %s",(val,us))
                    mysql.connection.commit()
                    return redirect('/es')
                elif len(r)==0:
                    flash(f"No record found for ISBN : {us}")
                    return redirect('/es')
            elif request.form.get("bkk"):
                return redirect('/ahom') 
        else:
            return render_template('estock.html',h=h,l1=l1)
    else:
        return redirect("/adlogin")
    
    
@app.route('/com',methods=['POST','GET'])
def com():
    flash("Comics : ")
    cur=mysql.connection.cursor()
    cur.execute("select * from stock where Genre like 'Comic'")
    mysql.connection.commit()
    r=cur.fetchall()
    session['s']=r
    session['p']=len(session['s'])
    l=[]
    if request.method=='POST':
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            r=cur.fetchall()
            for i in r:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
    else:
        return render_template('search.html')
    
@app.route('/nov',methods=['POST','GET'])
def nov():
    flash("Novels : ")
    cur=mysql.connection.cursor()
    cur.execute("select * from stock where Genre like 'Novel'")
    mysql.connection.commit()
    r=cur.fetchall()
    session['s']=r
    session['p']=len(session['s'])
    l=[]
    if request.method=='POST':
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            r=cur.fetchall()
            for i in r:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
    else:
        return render_template('search.html')

@app.route('/gen',methods=['POST','GET'])
def gen():
    flash("General : ")
    cur=mysql.connection.cursor()
    cur.execute("select * from stock where Genre like 'Gen'")
    mysql.connection.commit()
    r=cur.fetchall()
    session['s']=r
    session['p']=len(session['s'])
    l=[]
    if request.method=='POST':
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            r=cur.fetchall()
            for i in r:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
    else:
        return render_template('search.html')

@app.route('/stu',methods=['POST','GET'])
def stu():
    flash("Studies : ")
    cur=mysql.connection.cursor()
    cur.execute("select * from stock where Genre like 'Stu'")
    mysql.connection.commit()
    r=cur.fetchall()
    session['s']=r
    session['p']=len(session['s'])
    l=[]
    if request.method=='POST':
        if request.method=='POST':
            if request.form.get("se"):
                d = request.form['ser']
                d=d.lower()
                cur=mysql.connection.cursor()
                cur.execute("select * from stock")
                mysql.connection.commit()
                r=cur.fetchall()
                for i in r:
                    l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                    p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                    for q in l1:
                        if q not in p:
                            l1=l1+q
                    o=l1.lower()
                    for j in d.split(' '):
                        if j in o:
                            l.append(i)
                            break
                session['s']=l
                session['p']=len(session['s'])
                return redirect("/s")
    else:
        return render_template('search.html')

@app.route('/vall',methods=['POST','GET'])
def vall():
    flash("All : ")
    cur=mysql.connection.cursor()
    cur.execute("select * from stock")
    mysql.connection.commit()
    r=cur.fetchall()
    session['s']=r
    session['p']=len(session['s'])
    l=[]
    if request.method=='POST':
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            r=cur.fetchall()
            for i in r:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
    else:
        return render_template('search.html')

@app.route('/vsk',methods=['POST','GET'])
def vsk():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from stock")
        mysql.connection.commit()
        r=cur.fetchall()
        h=['ISBN', 'Name', 'Author Name', 'Edition', 'Publication', 'Price','Genre','Quantity', 'Image_url','About','Recomendation']
        l1=[]
        for i in r:
            l=[i['ISBN'], i['Name'], i['AName'], i['Edition'], i['Publication'], i['Price'], i['Genre'], i['Quantity'], i['Image_url'],i['About'],i['Rec']]
            l1.append(l)
        return render_template('vskk.html',h=h,l1=l1)
    else:
        return redirect("adlogin")
    
@app.route('/reset',methods=['POST','GET'])
def ress():
    if request.method=='POST':
        if request.form.get("so"):
            us = request.form['emal']
            session['ee']=us
            cur=mysql.connection.cursor()
            cur.execute("select * from user where unam like %s",(us,))
            mysql.connection.commit()
            r=cur.fetchall()
            l={'0','1','2','3','4','5','6','7','8','9'}
            ko=''
            for i in random.sample(l, 4):
                ko=ko+i
            session['ko']=ko
            if len(r)>0:
                """
                toaddr  =us
                passwor = "bbb@54321"
                msg = EmailMessage()
                msgt='Your OTP for password reset request is ' +ko+'.\n        -Brilliants Books'
                msg.set_content(msgt)
                msg['Subject'] = "RESET PASSWORD From Brilliant Books"
                msg['From'] = 'Brilliant Books'
                msg['To'] = toaddr
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("brilliantbooks0@gmail.com", passwor)
                server.send_message(msg)
                server.quit()
                """
                flash(ko+":OTP send to your mail")
                return redirect('/reset')
            else:
                flash("Email not registered")
                return redirect('/reset')
        if request.form.get("rs"):
            us = request.form['emal']              
            ot = request.form['otp']
            pas = request.form['pas'] 
            cpas = request.form['cpas']
            f=0
            if pas!=cpas:
                flash("*Wrong password")
                f=1
                return redirect('/reset')
            if ot==session['ko'] and f==0 and us==session['ee']:
                cur=mysql.connection.cursor()
                cur.execute("update user set pass=%s where unam like %s",(pas,us))
                mysql.connection.commit()
                flash("Password successfully reset")
                return redirect('/reset')
            elif us!=session['ee']:
                flash("Changed Email")
                return redirect('/reset')
            else:
                flash("Wrong OTP")
                return redirect('/reset')
            
    else:
        return render_template('forpass.html')
    
@app.route('/abt',methods=['POST','GET']) 
def abt():
    if request.method=='POST':
        l=[]
        if request.form.get("se"):
            d = request.form['ser']
            d=d.lower()
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            rm=cur.fetchall()
            for i in rm:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in d.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
    else:
        return render_template("about.html")


@app.route('/buynow',methods=['POST','GET'])
def cart():
    le=len(session['det'])
    l=[]
    tt=0
    for i in session['det']:
        for j in i:
            l.append(j)
    l1={v['ISBN']:v for v in l}.values()
    de=[]
    for i in l1:
        c=l.count(i)
        de.append([i,c])
    for i in de:
        tt=tt+int(i[0]['Price'])*int(i[1])
    
    if request.method=='POST':
        if request.form.get("bn"):
            session['order']=de
            return redirect("/order")
        if request.form.get("uc"):
            session['det']=[]
            return redirect("/buynow")
        if request.form.get("se"):
                d = request.form['ser']
                d=d.lower()
                cur=mysql.connection.cursor()
                cur.execute("select * from stock")
                mysql.connection.commit()
                r=cur.fetchall()
                for i in r:
                    l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                    p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                    for q in l1:
                        if q not in p:
                            l1=l1+q
                    o=l1.lower()
                    for j in d.split(' '):
                        if j in o:
                            l.append(i)
                            break
                session['s']=l
                session['p']=len(session['s'])
                return redirect("/s")
    else:
        return render_template("cart.html",de=de,le=le,tt=tt)

@app.route('/order',methods=['POST','GET'])
def orde():
    l=[]
    if 'order' not in session or len(session['order'])==0:
        return redirect("/")
    else:
        if request.method=='POST':
            if request.form.get("se"):
                d = request.form['ser']
                d=d.lower()
                cur=mysql.connection.cursor()
                cur.execute("select * from stock")
                mysql.connection.commit()
                r=cur.fetchall()
                for i in r:
                    l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                    p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                    for q in l1:
                        if q not in p:
                            l1=l1+q
                    o=l1.lower()
                    for j in d.split(' '):
                        if j in o:
                            l.append(i)
                            break
                session['s']=l
                session['p']=len(session['s'])
                return redirect("/s")
            if request.form.get("po"):
                 fd = request.form['fnam']
                 ln = request.form['lnam']
                 ed = request.form['emal']
                 pd = request.form['pon']
                 zd = request.form['zip']
                 ld = request.form['lan']
                 ad = request.form['add']
                 nam=fd+" "+ln
                 add="Address: "+ad+" Landmark: "+ld+" ZIP: "+zd
                 cur=mysql.connection.cursor()
                 ttt=0
                 for i in session['order']:
                     tt=int(i[0]['Price'])*int(i[1])
                     ttt=ttt+tt
                     cur.execute("insert into dor(name,isbn,bnam,price,qua,total,mno,emal,adres,sta) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,'Order Placed')",(nam,i[0]['ISBN'],i[0]['Name'],i[0]['Price'],i[1],tt,pd,ed,add))
                     mysql.connection.commit()
                     l.append([i[0]["Name"],i[0]["Price"],i[1],tt])
                 cur.execute("select * from dor where emal like %s or orid like %s and sta like 'Order Placed'",(ed,ed))
                 mysql.connection.commit()
                 rm=cur.fetchall()
                 s=''
                 for i in rm:
                     s=s+str(i['orid'])+","
                 """
                 toaddr  = ed
                 passwor = "bbb@54321"
                 msg = EmailMessage()
                 msgt='Your open Order IDs='+s+'\n'+str(l)+'\n'+"Total Amount: ₹"+str(ttt)+' \n Thank you for chosing us.\nBrilliants Books'
                 msg.set_content(msgt)
                 msg['Subject'] = "Thanks From Brilliant Books"
                 msg['From'] = 'Brilliant Books'
                 msg['To'] = toaddr
                 server = smtplib.SMTP('smtp.gmail.com', 587)
                 server.starttls()
                 server.login("brilliantbooks0@gmail.com", passwor)
                 server.send_message(msg)
                 server.quit()
                 toaddrs  = "brilliantbooks0@gmail.com"
                 password = "bbb@54321"
                 msg = EmailMessage()
                 msgtxt=str(l)+'\n'+"Total Amount: ₹"+str(ttt)+'\n'+'Order IDs='+s+'\n'+'From '+nam+'\n'+add+'\n'+'Contact: '+pd+'\n'+ed
                 msg.set_content(msgtxt)
                 msg['Subject'] = "From Orders"
                 msg['From'] = 'Brilliant Books'
                 msg['To'] = toaddrs
                 server = smtplib.SMTP('smtp.gmail.com', 587)
                 server.starttls()
                 server.login("brilliantbooks0@gmail.com", password)
                 server.send_message(msg)
                 server.quit()
                 session['det']=[]
                 """
                 msg1='Your open Order IDs='+s+'\n'+str(l)+'\n'+"Total Amount: Rs."+str(ttt)+' \n Thank you for chosing us.\nBrilliants Books'
                 url='https://www.fast2sms.com/dev/bulk'
                 para={'authorization':'dFjveUQ2gRbokDNMJ4CALmYfZSI3VpBOuWyPwznlHTrExG5cisLjXZOsiGHhSMgaJNu2Ve7Q6nd9obPr',
                          'sender_id':'FSTSMS',
                          'message':msg1,
                          'language':'english',
                          'route':'p',
                          'numbers':pd}
                 requests.get(url,params=para)
            

                 flash("Successfully Placed Order")
                 return redirect("/order")
        else:
            return render_template("orderdet.html")    

@app.route('/os',methods=['POST','GET'])
def es():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from dor where sta like 'Packed' or sta like 'Order Placed' or sta like  'Out for Delivery'")
        mysql.connection.commit()
        r=cur.fetchall()
        h=["Order ID","Name","ISBN","Book","Quantity",'Total','Mobile Number','Email','address', 'status']
        l1=[]
        for i in r:
            l=[i['orid'], i['name'], i['isbn'], i['bnam'], i['qua'], i['total'], i['mno'], i['emal'], i['adres'],i['sta']]
            l1.append(l)
        if request.method=='POST':
            if request.form.get("dl"):
                us = request.form['st']
                val = request.form['sta']
                cur=mysql.connection.cursor()
                cur.execute("select * from dor where orid like %s",(us,))
                mysql.connection.commit()
                r=cur.fetchall()
                if len(r)>0:
                    flash(f"Successfully edited {us}")
                    cur.execute("update dor set sta=%s where orid like %s",(val,us))
                    mysql.connection.commit()
                    if val=="Delivered":
                        cur.execute("select * from dor where orid like %s",(us,))
                        mysql.connection.commit()
                        ro=cur.fetchall()
                        cur.execute("select * from stock where ISBN like %s",(ro[0]["isbn"],))
                        mysql.connection.commit()
                        rs=cur.fetchall()
                        v=int(rs[0]["Quantity"])-int(ro[0]["qua"])
                        cur.execute("update stock set Quantity=%s where ISBN like %s",(str(v),ro[0]['isbn']))
                        mysql.connection.commit()
                    return redirect('/os')
                elif len(r)==0:
                    flash(f"No record found for order no. : {us}")
                    return redirect('/os')
            elif request.form.get("bkk"):
                return redirect('/ahom') 
        else:
            return render_template('ordsta.html',h=h,l1=l1)
    else:
        return redirect("/adlogin")

@app.route('/oh',methods=['POST','GET'])
def esh():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("select * from dor where sta like 'Delivered' or sta like 'Cancled by store' or sta like 'Cancled by User'")
        mysql.connection.commit()
        r=cur.fetchall()
        h=["Order ID","Name","ISBN","Book","Quantity",'Total','Mobile Number','Email','address', 'status']
        l1=[]
        for i in r:
            l=[i['orid'], i['name'], i['isbn'], i['bnam'], i['qua'], i['total'], i['mno'], i['emal'], i['adres'],i['sta']]
            l1.append(l)
        if request.method=='POST':
            if request.form.get("dl"):
                cur=mysql.connection.cursor()
                cur.execute("delete from dor where sta like 'Delivered' or sta like 'Cancled by store'")
                flash("Successfully deleted")
                mysql.connection.commit()
                return redirect('/oh')
            elif request.form.get("bkk"):
                return redirect('/ahom') 
        else:
            return render_template('odrhis.html',h=h,l1=l1)
    else:
        return redirect('/adlogin')

@app.route('/tk',methods=['POST','GET'])
def track():
    if request.method=='POST':
        if request.form.get("se"):
            l=[]
            sd = request.form['ser']
            cur=mysql.connection.cursor()
            cur.execute("select * from stock")
            mysql.connection.commit()
            rj=cur.fetchall()
            for i in rj:
                l1 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                for q in l1:
                    if q not in p:
                        l1=l1+q
                o=l1.lower()
                for j in sd.split(' '):
                    if j in o:
                        l.append(i)
                        break
            session['s']=l
            session['p']=len(session['s'])
            return redirect("/s")
        if request.form.get("ln"):
            d = request.form['id']
            cur=mysql.connection.cursor()
            cur.execute("select * from dor where emal like %s or orid like %s",(d,d))
            mysql.connection.commit()
            r=cur.fetchall()
            if len(r)>0:
                session['d']=d
                return redirect('/tkr')
            elif len(r)==0:
                flash(f"No open order found for: {d}")
                return redirect('/tk')
    else:
        return render_template('trackid.html')

@app.route('/tkr',methods=['POST','GET'])
def trac():
    
    cur=mysql.connection.cursor()
    cur.execute("select * from dor where emal like %s or orid like %s",(session['d'],session['d']))
    mysql.connection.commit()
    r=cur.fetchall()
    h=["Order ID","Name", "ISBN","Book","Quantity",'Total','Mobile Number','Email','address', 'status']
    l1=[]
    for i in r:
        l3=[i['orid'], i['name'], i['isbn'], i['bnam'], i['qua'], i['total'], i['mno'], i['emal'], i['adres'],i['sta']]
        l1.append(l3)
    if request.method=='POST':
        l=[]
        if request.form.get("se"):
                ds = request.form['ser']
                cur=mysql.connection.cursor()
                cur.execute("select * from stock")
                mysql.connection.commit()
                rs=cur.fetchall()
                for i in rs:
                    l2 =' '.join([str(elem) for elem in [i[key] for key in ['ISBN','Name','AName','Publication','Genre','About']]])
                    p='`~!@$%^&*()_-+={}:<>?||[]\;#,./'
                    for q in l2:
                        if q not in p:
                            l2=l2+q
                    o=l2.lower()
                    for j in ds.split(' '):
                        if j in o:
                            l.append(i)
                            break
                session['s']=l
                session['p']=len(session['s'])
                return redirect("/s")
        if request.form.get("dl"):
            d = request.form['st']
            cur=mysql.connection.cursor()
            cur.execute("Select * from dor where orid like %s",(d,))
            mysql.connection.commit()
            r=cur.fetchall()
            if len(r)>0:
                flash(f"Successfully cancled {d}")
                cur.execute("update dor set sta='Cancelled by User' where orid like %s",(d,))
                mysql.connection.commit()
                return redirect('/tkr')
                
            elif len(r)==0:
                flash(f"No record found for order no. : {d}")
                return redirect('/tkr')
        if request.form.get("bkk"):
            return redirect('/tk')
    else:
        return render_template('track.html',h=h,l1=l1)    
@app.route('/stk',methods=['POST','GET'])
def tec():
    if 'ho' in session:
        cur=mysql.connection.cursor()
        cur.execute("Select qua from dor where sta like 'Delivered'")
        mysql.connection.commit()
        r=cur.fetchall()
        k=0
        try:
            for i in r:
                k=k+int(i['qua'])
        except:
            k=0
        cur=mysql.connection.cursor()
        cur.execute("Select Quantity from stock")
        mysql.connection.commit()
        r=cur.fetchall()
        s=0
        for i in r:
            s=s+int(i['Quantity'])
        o=s+k
        data = {'Total Stock' : 'Sold', 'Left Stocks' : s, 'Sold Stocks' : k}
        return render_template("any.html",data=data,o=o)
    else:
        return redirect('/adlogin')
    
    
if __name__=='__main__':
    app.run()
