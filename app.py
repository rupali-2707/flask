from flask import Flask, render_template,request

from flask_mail import Mail,Message

app= Flask(__name__)


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'grupali645@gmail.com',  #enter email
    "MAIL_PASSWORD": '' #enter password
}
app.config.update(mail_settings)
mail= Mail(app)

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/send_mail',methods=['GET','POST'])
def send_mail():
    if request.method=="POST":
        email=request.form['email']
        subject=request.form['subject']
        msg=request.form['message']

        message=Message(subject,sender="grupali645@gmail.com",recipients=[email])
        message.body=msg

        mail.send(message)
        success="Mail sent"
        return render_template("result.html",success=success)

if __name__=="__main__":
    app.run(debug=True)
