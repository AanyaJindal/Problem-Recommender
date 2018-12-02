import functools
import pickle
import scipy.sparse as sp

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('user', __name__, url_prefix='/user')

sparse_user_item = sp.load_npz('confi.npz')
model = pickle.load(open('model.pkl','rb'))
problem_name = pickle.load(open('problem_name.pkl','rb'))
user_id = pickle.load(open('user_id.pkl','rb'))

@bp.route('/preds', methods=('GET', 'POST'))
def preds():
    links = []
    username = ""
    if request.method == 'POST':
        username = request.form['username']
        error = None

        if not username:
            error = 'Username is required.'

        if error is None:
            
            rec = model.recommend(user_id[username], sparse_user_item)
            print(rec)
            links = []
            for r in rec:
                name = problem_name[r[0]]
                contest = ""
                problem = ""
                for x in range(len(name)):
                    if name[x].isalpha():
                        problem = name[x:]
                        contest = name[:x]
                links.append("https://codeforces.com/contest/" + str(contest) + "/problem/" + str(problem))
        else:
            flash(error)

    return render_template('user/preds.html', links = links, username=username)

@bp.route('/test', methods=('GET', 'POST'))
def test():
    posts = model.recommend(24593, sparse_user_item)
    return render_template('user/test.html',hdr = "yoyoyo",posts=posts)