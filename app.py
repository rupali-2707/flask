from flask import Flask, render_template,request
from flask import flash, redirect, request
from flask_mail import Mail,Message
import os
import csv


app= Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

def stmp_setting(stmp_email,port,sender,password):
    # mail_settings = {
    #     "MAIL_SERVER": 'smtp.gmail.com',
    #     "MAIL_PORT": 465,
    #     "MAIL_USE_TLS": False,
    #     "MAIL_USE_SSL": True,
    #     "MAIL_USERNAME": '',  #enter email
    #     "MAIL_PASSWORD": '' #enter password
    # }
    mail_settings = {
        "MAIL_SERVER": stmp_email,
        "MAIL_PORT": int(port),
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": sender, 
        "MAIL_PASSWORD": password 
    }
    app.config.update(mail_settings)


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/send_mail',methods=['GET','POST'])
def send_mail():
    

    if request.method=="POST":
        stmp=request.form['smtp_email']
        port=request.form['port']
        sender=request.form['sender_email']
        password=request.form['password']
        
        subject=request.form['subject']
        msg=request.form['message']

        stmp_setting(stmp,port,sender,password)
        mail= Mail(app)


        if request.form["submit_button"]=='test':    #for testing
            email=request.form['email']
            email=email.splitlines() #convert into list
            print(email)
            message=Message(subject,sender=sender,recipients=email)  #passing list of receipents
            message.body=msg

            if not (mail.send(message)):
                flash("Test Mail sent Successful","success")
                return redirect(request.url)
            flash("Test Mail send Failed","danger")
        


        if request.form["submit_button"]=='bulk sending':
            target=os.path.join(APP_ROOT,'csv_file/')
            print("target:\t",target)

            if not os.path.isdir(target):
                os.mkdir(target)
            for file in request.files.getlist("file"):
                print(file)
                filename=file.filename
                print(filename) #file name
                des="/".join([target,filename])
                print("des\t:",des)
                file.save(des)
                try:
                    with open(r'C:\Users\lenovo\Desktop\flask\csv_file\{}'.format(filename), newline='') as f:
                            print("hey")
                            reader = csv.reader(f)
                            list1 = list(reader)

                    print(list1) 
                    flat_list = []
                    for sublist in list1:
                            for item in sublist:
                                flat_list.append(item)
                    print(flat_list)

                    if request.form["submit_button"]=='bulk sending':
                        if not flat_list:
                                    flash("you did not load properly","danger")
                        else:
                                        message=Message(subject,sender=sender,recipients=flat_list)  #passing list of receipents
                                        message.body=msg

                                        if not (mail.send(message)):
                                            flash("Bulk Mail sent Successful","success")
                                            # return redirect(request.url)
                                        else:
                                             flash("Bulk Mail send Failed","danger")
                                        # return redirect(request.url)
                except:
                    flash("you did not load properly","danger")
                    return redirect(request.url)

    return render_template("home.html")
if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',port=50000, debug=True)
