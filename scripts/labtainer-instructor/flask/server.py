#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
from flask import Flask, render_template, url_for, send_file, Response
import json
import sys
import os
import glob
from flask_table import Table, Col, LinkCol, create_table, NestedTableCol

'''
Use the Flask framework to create dynamic web pages displaying student goals
and the intermediate results and raw artifacts.
'''

app = Flask(__name__)
data_dir = '/home/mike/tmp'
#lab = 'telnetlab'
lab = 'ssh-agent'

tbl_options = dict(no_items='Empty',   border='1px solid black')

@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/grades')
def grades():
    class HackLinkCol(LinkCol):
        def td_format(self, content):
            if ':' in content:
                return content.rsplit(':', 1)[1]
            else:
                return content

    lab_dir = os.path.join(data_dir, lab)
    json_fname = '%s.grades.json' % lab
    grade_json = os.path.join(lab_dir, json_fname)
    rows = []
    #TableCls = create_table('TableCls')\
    #        .add_column('name', Col('Name'))
    GoalTableCls = create_table('GoalTableCls', options=tbl_options)\
            .add_column('name', LinkCol('Name', 'student_select',
                   url_kwargs=dict(student_id='full_name'), attr='name'))

    with open(grade_json) as fh:
        grade_dict = json.load(fh)
        first_key = list(grade_dict.keys())[0]
        for goal in grade_dict[first_key]['grades']:
            if not goal.startswith('_'):
                #GoalTableCls.add_column(goal, Col(goal))
                GoalTableCls.add_column(goal, HackLinkCol(goal, 'goal_select',
                   url_kwargs=dict(student_id='full_name', goal=goal), attr=goal))
        for student in grade_dict:
            row = {}
            parts = student.split('_at_')
            row['name'] = parts[0]
            row['full_name'] = student
            for key in grade_dict[student]['grades']:
                if not key.startswith('_'):
                    row[key] = '%s:%s' % (key, grade_dict[student]['grades'][key])
            rows.append(row)
        tbl = GoalTableCls(rows) 
            

    return render_template('grades.html', title='Grades',
                           table=tbl)

def findTS(student_dir, student_id, container_list, ts):
    glob_mask = '*.%s' % ts
    sub_tbl = []
    for container_id in container_list:
        result_dir = os.path.join(student_dir, container_id, '.local', 'result')
        ts_list = glob.glob(os.path.join(result_dir, glob_mask))
        container = container_id.split('.')[1]
        for ts_path in ts_list:
            row = {}
            ts = os.path.basename(ts_path) 
            fname = ts.rsplit('.',1)[0]
            row['container'] = container
            row['container_id'] = container_id
            row['fname'] = fname
            row['ts'] = ts
            row['result_dir'] = result_dir
            row['student_id'] = student_id
            sub_tbl.append(row)
    return sub_tbl
            
@app.route('/grades/<string:student_id>')
def student_select(student_id):

    class RawSubTable(Table):
        container = Col('')
        fname = LinkCol('', 'raw_select',
                   url_kwargs=dict(student_id='student_id',container_id='container_id',
                      ts='ts', fname='fname'), attr='fname')

    BoolTableCls = create_table('BoolTableCls', options = tbl_options)
    BoolTableCls.add_column('name', Col('Name'))
    BoolTableCls.add_column('value', Col('Value'))

    lab_dir = os.path.join(data_dir, lab)
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')
    bool_results_file = os.path.join(student_inter_dir, lab)
    bool_tbl = []
    with open(bool_results_file) as fh:
        br = json.load(fh)
        for b in br:
            row = {}
            if b.startswith('_') or b == 'PROGRAM_ENDTIME':
                continue
            row['name'] = b
            row['value'] = br[b]
            bool_tbl.append(row)
    tbl = BoolTableCls(bool_tbl)

    container_list = os.listdir(student_dir)
    
    TS_TableCls = create_table('TS_TableCls', options=tbl_options)\
            .add_column('ts', LinkCol('ts', 'ts_select',
                   url_kwargs=dict(ts='ts', student_id='student_id'), attr='ts'))

    TS_TableCls.add_column('raw_links', NestedTableCol('Raw artifacts', RawSubTable))

    glob_mask = '%s.*' % lab 
    ts_list = glob.glob(os.path.join(student_inter_dir, glob_mask))
    ts_rows = []
    for ts in ts_list:
        base = os.path.basename(ts)
        ts_suffix = base.rsplit('.')[-1]
        raw_tbl = findTS(student_dir, student_id, container_list, ts_suffix)
        row = {}
        row['ts'] = ts_suffix
        row['raw_links'] = raw_tbl
        row['student_id'] = student_id
        ts_rows.append(row)
    ts_tbl = TS_TableCls(ts_rows)

    hist_list = []
    for full_container in container_list:
        if os.path.isfile(os.path.join(student_dir, full_container, '.bash_history')):
            container = full_container.split('.')[1]
            url = '%s/%s/history' % (student_id, full_container)
            entry = [container, url]
            hist_list.append(entry)
    print('entries is %d' % len(hist_list))

    return render_template('student.html', title=student_id, table = tbl, ts_table = ts_tbl, 
          hist_list = hist_list, back_grades=url_for('grades'))

@app.route('/grades/<student_id>/ts/<string:ts>')
def ts_select(student_id, ts):
    lab_dir = os.path.join(data_dir, lab)
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')
    ts_file = '%s.%s' % (lab, ts)
    ts_path = os.path.join(student_inter_dir, ts_file)
    print('ts_path %s' % ts_path)
    with open(ts_path) as fh:
        data = fh.read()
    
    return render_template('ts.html', student_id=student_id, ts=ts, data = data)
    

@app.route('/grades/<student_id>/<container_id>/history')
def history(student_id, container_id):
    lab_dir = os.path.join(data_dir, lab)
   
    container_history = os.path.join(lab_dir, student_id, container_id, '.bash_history')
    with open(container_history) as fh:
        data = fh.read()
    
    return render_template('history.html', student_id=student_id, data = data)


@app.route('/grades/<student_id>/raw/<container_id>/<ts>/<fname>')
def raw_select(student_id, container_id, ts, fname):
    lab_dir = os.path.join(data_dir, lab)
    result_dir = os.path.join(lab_dir, student_id, container_id, '.local', 'result')
    path = os.path.join(result_dir, ts)
    print('path %s' % path)
    with open(path) as fh:
        data = fh.read()
    
    return render_template('history.html', student_id=student_id, data = data)


def getGoal(goals_json, goal_id):
    for goal_entry in goals_json:
        if goal_entry['goalid'] == goal_id:
            return goal_entry
    return None


@app.route('/grades/<student_id>/goals/<goal>')
def goal_select(student_id, goal):
    lab_dir = os.path.join(data_dir, lab)
    student_dir = os.path.join(lab_dir, student_id)
    student_inter_dir = os.path.join(student_dir, '.local','result')
    goals_json_file = os.path.join(student_inter_dir, 'goals.json')
    goal_id = goal.split(':')[0]
    with open(goals_json_file) as fh:
        goals_json = json.load(fh)
        goal_entry = getGoal(goals_json, goal_id) 
        if len(goal_entry['boolean_string']) > 0: 
           data = 'boolean: %s' % goal_entry['boolean_string'] 
    
    return render_template('goal.html', student_id=student_id, goal = goal, 
               data=data,back_grades=url_for('grades'))

if __name__ == '__main__':
    app.run(debug=True, port=8008, host='0.0.0.0')
       
