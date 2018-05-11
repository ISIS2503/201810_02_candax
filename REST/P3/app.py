from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from requests import put, get, post
from flask_restful import fields, marshal_with
from datetime import datetime
from flask_restful import reqparse
# from multiprocessing import Process, Value
import time
import threading
import json


def ordenarPorHi(arr):
    arr.sort(key=lambda x: x['hi'])


def ordenarPorHf(arr):
    arr.sort(key=lambda x: x['hf'])


app = Flask(__name__)
api = Api(app)

# resource_fields = {
#     'owner':   fields.String,
#     'pos':    fields.Integer,
#     'pass':   fields.String,
#     'hi': fields.DateTime,
#     'hf': fields.DateTime

# }


@app.before_first_request
def activate_job():
    def run_job():
        while True:
            # print("activas " + str(len(PASSWORDS_ACTIVOS))+ " pasivas " +
            # str(len(PASSWORDS_INACTIVOS)))
            ya = str(datetime.now())
            print(ya + " activos " + str(len(PASSWORDS_ACTIVOS)) +
                                         " inactivos " +
                                         str(len(PASSWORDS_INACTIVOS)))
            if(len(PASSWORDS_ACTIVOS) >= 1):
                while(len(PASSWORDS_ACTIVOS) >= 1 and PASSWORDS_ACTIVOS[0]["hf"] < ya):
                    print("entra a sacar activo")
                    pwd = PASSWORDS_ACTIVOS.pop(0)
                    pwd["pass"] = "0000"
                    print(pwd)
                    print(json.dumps(pwd))
                    post('http://172.24.41.149:8000/publishPasswords', json=(pwd))
            if(len(PASSWORDS_INACTIVOS) >= 1):
                while(len(PASSWORDS_INACTIVOS) >= 1 and PASSWORDS_INACTIVOS[0]["hi"] < ya):
                    print("entra a sacar inactivo")
                    pwd = PASSWORDS_INACTIVOS.pop(0)
                    PASSWORDS_ACTIVOS.append(pwd)
                    print(pwd)
                    print(json.dumps(pwd))
                    post('http://172.24.41.149:8000/publishPasswords', json=(pwd))

            time.sleep(3)

    thread = threading.Thread(target=run_job)
    thread.start()


def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = get('http://localhost:5000/pwds')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()


PASSWORDS_ACTIVOS = []
PASSWORDS_INACTIVOS = []


parser = reqparse.RequestParser()
parser.add_argument('owner')
parser.add_argument('pos')
parser.add_argument('pass')
parser.add_argument('hi')
parser.add_argument('hf')


class Passwd(Resource):
    # def get(self, pwds_id):
    #     # abort_if_todo_doesnt_exist(pwds_id)
    #     return TODOS[pwds_id]

    # def delete(self, pwds_id):
    #     # abort_if_todo_doesnt_exist(pwds_id)
    #     del TODOS[pwds_id]
    #     return '', 204

    # @marshal_with(resource_fields)
    def post(self):
        global PASSWORDS_ACTIVOS, PASSWORDS_INACTIVOS
        args = parser.parse_args()
        # task = {'task': args['task']}
        print("args:" + str(args))
        pwd = {"owner": args["owner"],
               "pos": args["pos"],
               "pass": args["pass"],
               "hi": args["hi"],
               "hf": args["hf"], }
        # print(owner)
        if(args["hi"] < str(datetime.now())):
            print("aaaaaaa" + args["hi"] +  str(datetime.now()))
            print("bbbbbbbb" + str(args["hi"]< str(datetime.now())))
            print("entra activos post")
            PASSWORDS_ACTIVOS.append(pwd)
            ordenarPorHf(PASSWORDS_ACTIVOS)
            print(pwd)
            print(json.dumps(pwd))
            post('http://172.24.41.149:8000/publishPasswords', json=pwd)
#

        else:
            print("aaaaaaa" + args["hi"] +  str(datetime.now()))
            print("bbbbbbbb" + str((args["hi"]< str(datetime.now()))))
            print("entra inactivos post")
            PASSWORDS_INACTIVOS.append(pwd)
            ordenarPorHi(PASSWORDS_INACTIVOS)

        return pwd, 200

    def get(self):
        return "up and running", 200


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
# class TodoList(Resource):
#     def get(self):
#         return TODOS

#     def post(self):
#         args = parser.parse_args()
#         pwds_id = int(max(TODOS.keys()).lstrip('todo')) + 1
#         pwds_id = 'todo%i' % pwds_id
#         TODOS[pwds_id] = {'task': args['task']}
#         return TODOS[pwds_id], 201

##
## Actually setup the Api resource routing here
##
# api.add_resource(TodoList, '/pwds')
api.add_resource(Passwd, '/pwds')



# def record_loop(loop_on):
#    while True:
#       if loop_on.value == True:
        # ya = str(datetime.now())
        # print(ya + " activos " + str(len(PASSWORDS_ACTIVOS)) + " inactivos " + str(len(PASSWORDS_INACTIVOS)))
        # if(len(PASSWORDS_ACTIVOS)>=1):
        #     while(len(PASSWORDS_ACTIVOS)>=1 and PASSWORDS_ACTIVOS[0]["hf"]<ya):
        #         pwd = PASSWORDS_ACTIVOS.pop(0)
        #         pwd["pass"] = "0000"
        #         # post('http://localhost:8000/passwords', data=pwd).json()
        # if(len(PASSWORDS_INACTIVOS)>=1):
        #     while(len(PASSWORDS_INACTIVOS)>=1 and PASSWORDS_INACTIVOS[0]["hi"]<ya):
        #         pwd = PASSWORDS_INACTIVOS.pop(0)
        #         # post('http://localhost:8000/passwords', data=pwd).json()




#       time.sleep(1)

if __name__ == '__main__':
    # recording_on = Value('b', True)
    # p = Process(target=record_loop,args=(recording_on,))
    # p.start()
    start_runner()
    app.run(debug=True)
