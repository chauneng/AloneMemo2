from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

#client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://maro:chauneng@54.180.121.145', 27017)
db = client.memover2db


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['POST'])
def post_memo():

    title_receive = request.form['title_give']
    content_receive = request.form['content_give'] 

    memo = {'title': title_receive, 'content': content_receive}

    db.memover2db.insert_one(memo)

    return jsonify({'result': 'success'})

@app.route('/memo', methods=['GET'])
def read_memos():

    # 수정, 삭제시 같은 값을 가지는 메모가 없도록 Mongodb에서 임의로 설정한 _id 값을 불러와 사용.
    results = list(db.memover2db.find({}))

    # '_id'필드의 objectId는 json으로 바꿀 경우 오류가 발생하기 때문에 str타입으로 변경해서 저장.
    for result in results:
        result['_id'] = str(result['_id'])


    return jsonify({'result': 'success', 'memos': results})

@app.route('/memo/mod', methods=['POST'])
def mod_memo():

    #str로 변경되어있던 objectid를 다시 objectid로 변경.
    m_id_receive = ObjectId(request.form['id_modded'])
    m_title_receive = request.form['title_modded']
    m_content_receive = request.form['content_modded']

    db.memover2db.update_one({'_id':m_id_receive},{'$set':{'title':m_title_receive, 'content':m_content_receive}})
    
    return jsonify({'result': 'success'})

@app.route('/memo/delete', methods=['POST'])
def del_memo():
    
    #str로 변경되어있던 objectid를 다시 objectid로 변경.
    d_id_receive = ObjectId(request.form['id_deleted'])

    db.memover2db.delete_one({'_id':d_id_receive})
   
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)