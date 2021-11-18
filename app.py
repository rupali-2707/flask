from flask import Flask, render_template,request
from flask import flash, redirect, request
from flask_mail import Mail,Message

app= Flask(__name__)

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

        stmp_setting(stmp,port,sender,password)
        mail= Mail(app)
        email=request.form['email']
        subject=request.form['subject']
        msg=request.form['message']
        email=email.splitlines() #convert into list
        print(email)

        message=Message(subject,sender=sender,recipients=email)  #passing list of receipents
        message.body=msg

        if not (mail.send(message)):
            flash("Mail sent Successful","success")
            return redirect(request.url)
        flash("Mail send Failed","danger")
        return redirect(request.url)

    return render_template("home.html")
if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',port=50000, debug=True)
