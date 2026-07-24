from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/')
def home(): return render_template('index.html')

@app.route('/track',methods=['POST'])
def track():
    n=request.form['name'];g=int(request.form['goal']);gl=int(request.form['glasses'])
    rem=max(g-gl,0)
    ok=gl>=g
    return render_template('index.html',name=n,goal=g,glasses=gl,remaining=rem,status='Completed' if ok else 'Not Completed',message='Great job!' if ok else 'Keep going!')

if __name__=='__main__': app.run(debug=True)