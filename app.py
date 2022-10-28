from flask import Flask, render_template, request, redirect, url_for
import sys

from numpy import rec
from model import get_recommendations
app = Flask(__name__)

@app.route('/')
def index():
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("index.html")

@app.route('/profile', methods=["POST", "GET"])
def login():
    #print(f'request {request}', file=sys.stderr)
    if request.method == "POST":
        text = request.form['interest_bio']
        firstprio = request.form['one']
        secondprio = request.form['two']
        thirdprio = request.form['three']
        borough = request.form['category1']
        age = request.form['category']

        user_info_send = {
            "Bio": text,
            "Age": age,
            "Location": borough,
            "Pri1": firstprio,
            "Pri2": secondprio,
            "Pri3": thirdprio
        }
        
        rec = get_recommendations(user_info_send) # org_dict = Organization's Name, Similarity Score, and Explainability
        print(rec)
    
        return render_template("index.html",orgName1=rec["Organization's Name"][0],orgName2=rec["Organization's Name"][1],orgName3=rec["Organization's Name"][2],orgName4=rec["Organization's Name"][3],orgName5=rec["Organization's Name"][4],sim1= rec["Similarity Score"][0],sim2= rec["Similarity Score"][1],sim3= rec["Similarity Score"][2],sim4= rec["Similarity Score"][3],sim5= rec["Similarity Score"][4],exp =rec["Explainability of AI"])

    else:
        return render_template("profile.html") 


# user1 = {
#         "Bio": '"I enjoy working with technological and electronic items as I am interested in learning about Robotics. I participated as a guest speaker in a webinar about machine learning. I want to move patients from one location to another in the hospital I volunteered at St. Amant for two years where I assisted individuals living with developmental disabilities and autism."',
#         "Age" : 1,
#         "Location" : "BROOKLYN"
#     }

@app.route("/<usr>")
def user(usr):
    
    return f"<h1>{usr}</h1>"


@app.route('/about',methods=["POST", "GET"])
def about():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("about_us.html")


@app.route('/download',methods=["POST", "GET"])
def download_feed():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("download_feed.html")


@app.route('/heart',methods=["POST", "GET"])
def heart():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("heart_feedback.html")


@app.route('/details',methods=["POST", "GET"])
def feed_details():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("feed-details.html")


@app.route('/two',methods=["POST", "GET"])
def feed_det2():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("feed-details2.html")

@app.route('/three',methods=["POST", "GET"])
def feed_det3():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("feed-details3.html")

@app.route('/four',methods=["POST", "GET"])
def feed_det4():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("feed-details4.html")

@app.route('/five',methods=["POST", "GET"])
def feed_det5():
    
    #print(f'request {request}', file=sys.stderr, flush=True)
    return render_template("feed-details5.html")





if __name__ == "__main__":
    app.run(debug = True)










