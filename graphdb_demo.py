from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取用户输入的 SPARQL 端点 URL、仓库 ID 和查询
        sparql_endpoint = request.form['sparql_endpoint']
        repository_id = request.form['repository_id']
        sparql_query = request.form['sparql_query']

        # 连接到 RDF4J 仓库
        sparql = SPARQLWrapper(f"{sparql_endpoint}/{repository_id}")
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        output = ''
        for result in results["results"]["bindings"]:
            for k in result.keys():
                output += f'{k} : {result[k]["value"]} \n'

        return render_template('index.html', results=output)

    return render_template('index.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)
