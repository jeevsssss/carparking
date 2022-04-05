from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

login_flag = 0
signup_flag = 0
option_flag_1 = 0
option_flag_2 = 0


@app.route('/')
def welcome():
    global login_flag
    login_flag = 1
    return render_template('loginpage.html')


@app.route('/loginpage', methods=['POST', 'GET'])
def loginpage():
    global login_flag
    if login_flag and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "" and password == "":
            return render_template('options.html')
        else:
            return render_template('loginpage.html')
    else:
        return render_template('loginpage.html')

@app.route('/signuppage', methods=['POST', 'GET'])
def signuppage():
    global signup_flag
    if signup_flag and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "" and password == "":
            return render_template('signup.html')
        else:
            return render_template('signup.html')
    else:
        # signup_flag = 1
        return render_template('signup.html')

@app.route('/options', methods=['POST', 'GET'])
def options():
    global heap_size
    if login_flag:
        return render_template('options.html', name=heap_size)
    else:
        return render_template('loginpage.html')


@app.route('/choice1', methods=['POST', 'GET'])
def choice1():
    global option_flag_1
    option_flag_1 = 1
    return render_template('choice1.html')


@app.route('/givloc', methods=['POST', 'GET'])
def givloc():
    global arr
    global heap_size
    global option_flag_1
    global diction
    global curr_used
    if option_flag_1 and request.method == 'POST':
        carnum = request.form['carnum']
        try:
            diction[carnum]
        except:
            minimum = extract_min()
            diction[carnum] = minimum
            curr_used[minimum] = 1
            option_flag_1 = 0
            return render_template('givloc.html', name=[minimum, carnum, curr_used])
        else:
            return "<h1>Your Car is Already there</h1>"
    else:
        return render_template('options.html')


@app.route('/choice2', methods=['POST', 'GET'])
def choice2():
    return render_template('choice2.html')


@app.route('/givcar', methods=['POST', 'GET'])
def givcar():
    carnum = request.form['carnum']
    try:
        diction[carnum]
    except:
        return "<h1>Car not there in Parking Area</h1>"
    else:
        plotnum = diction[carnum]
        return render_template('givcar.html', name=plotnum)


@app.route('/choice3', methods=['POST', 'GET'])
def choice3():
    global option_flag_2
    option_flag_2 = 1
    return render_template('choice3.html')


@app.route('/givexit', methods=['POST', 'GET'])
def givexit():
    global arr
    global heap_size
    global option_flag_2
    global diction
    global curr_used
    if option_flag_2 and request.method == 'POST':
        carnum = request.form['carnum']
        try:
            diction[carnum]
        except:
            return "<h1>Car not there in Parking Area</h1>"
        else:
            plotnum = diction[carnum]
            curr_used[plotnum] = 0
            del diction[carnum]
            insert(plotnum)
            option_flag_2 = 0
            return render_template('givexit.html', name=[plotnum, curr_used])
    else:
        return render_template('options.html')


def heapify(i):
    global heap_size
    global arr
    smallest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if (l < heap_size and arr[l] < arr[smallest]):
        smallest = l
    if (r < heap_size and arr[r] < arr[smallest]):
        smallest = r
    if (smallest != i):
        swap = arr[i]
        arr[i] = arr[smallest]
        arr[smallest] = swap
        heapify(smallest)


def insert(key):
    global arr
    global heap_size
    heap_size += 1
    arr[heap_size - 1] = key
    heapify_bottom(heap_size - 1)


def heapify_bottom(i):
    global arr
    global heap_size
    parent = (i - 1) // 2
    if (parent >= 0):
        if (arr[parent] > arr[i]):
            swap = arr[parent]
            arr[parent] = arr[i]
            arr[i] = swap
            heapify_bottom(parent)


def extract_min():
    global arr
    global heap_size
    if heap_size==0:
        return(-1)
    minimum = arr[0]
    arr[0] = arr[heap_size-1]
    heap_size = heap_size-1
    heapify(0)
    return(minimum)


def buildHeap():
    global heap_size
    global arr
    startIdx = int((heap_size / 2)) - 1
    for i in range(startIdx, -1, -1):
        heapify(i)


if __name__ == "__main__":
    global heap_size
    global arr
    global diction
    global curr_used
    curr_used = {}
    diction = {}
    arr = []
    c = chr(65)
    for i in range(1, 7):
        for j in range(1, 9):
            s = c + str(j)
            arr.append(s)
            curr_used[s] = 0
        c = chr(65 + i)
    heap_size = len(arr)
    buildHeap()
    app.run(debug=True)
