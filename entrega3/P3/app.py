from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from requests import put, get, post
from flask_restful import fields, marshal_with
from datetime import datetime
from flask_restful import reqparse
from multiprocessing import Process, Value
import time

def ordenarPorHi(arr):
    arr.sort(key = lambda x : x['hi'])


def ordenarPorHf(arr):
    arr.sort(key = lambda x : x['hf'])



app = Flask(__name__)
api = Api(app)

resource_fields = {
    'owner':   fields.String,
    'pos':    fields.Integer,
    'pass':   fields.String,
    'hi': fields.DateTime,
    'hf': fields.DateTime

}

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
        args = parser.parse_args()
        # task = {'task': args['task']}
        pwd = { "owner" : args["owner"],
                "pos" : args["pos"],
                "pass" : args["pass"],
                "hi" : args["hi"],
                "hf" : args["hf"],
        }
        if(args["hi"]< str(datetime.now())):
            PASSWORDS_ACTIVOS.append(pwd) 
            ordenarPorHf(PASSWORDS_ACTIVOS)
            # post('http://localhost:5000/todo1', data=pwd).json()   
            
        
        else:
            PASSWORDS_INACTIVOS.append(pwd)
            ordenarPorHi(PASSWORDS_INACTIVOS)

        return pwd, 200


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



def record_loop(loop_on):
   while True:
      if loop_on.value == True:
        ya = str(datetime.now())
        while(PASSWORDS_ACTIVOS[0]["hf"]<ya):
            pwd = PASSWORDS_ACTIVOS.pop(0)
            pwd["pass"] = "0000"
            # post('http://localhost:5000/todo1', data=pwd).json()   
        while(PASSWORDS_INACTIVOS[0]["hi"]<ya):
            pwd = PASSWORDS_INACTIVOS.pop(0)
            # post('http://localhost:5000/todo1', data=pwd).json()   




      time.sleep(1)

if __name__ == '__main__':
    recording_on = Value('b', True)
    p = Process(target=record_loop,args=(recording_on,))
    p.start() 
    app.run(debug=True, use_reloader=False)