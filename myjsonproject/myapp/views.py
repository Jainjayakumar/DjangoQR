# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
import psycopg2
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode


def homePageView(request):
    return HttpResponse('Hello, World! This is Home Page')

@csrf_exempt
def methodinfo(request):
    if request.method == 'POST':
         return HttpResponse(request.body)
    return HttpResponse("Http request is: "+request.method)  

def myview(request):
    if request.method == 'GET':
        # <view logic>
        qrid = request.GET.get("QRID",' ')
        response = HttpResponse()
        response.write("Hello, World <br>")
        password ="jainjayakumar"
        cipher = b64decode(qrid.encode())
        dqrid = decrypt(password, cipher)
        try:
            conn = psycopg2.connect(database = "databasejson", user = "postgres", password = "raspberry", host = "127.0.0.1", port = "5432")
            response.write("\n<br>Opened database successfully<br>\n")
            cur = conn.cursor()
            cur.execute("SELECT * from PRODUCT WHERE QRID = '"+ str(dqrid.decode('utf-8'))+"';")
            rows = cur.fetchall()
            for row in rows:
                response.write("\n<br>QRID = "+ row[0] +"\n<br>SheetID = "+ row[1] + "\n<br>BatchID = " + row[2] + "\n<br>Company = " + row[3] + "\n<br>Status = "+ str(row[4]))
            response.write("\n\n<br><br>Operation done successfully")
        except (Exception, psycopg2.Error) as error :
            response.write("\n<br>Error while fetching data from PostgreSQL", error)
        finally:
	        #closing database connection.
	        if(conn):
	            cur.close()
	            conn.close()
	            response.write("\n<br><br>PostgreSQL connection is closed")
        return response

@csrf_exempt
def my_view(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        #json_str = json.dumps(data)
        resp = json.loads(data)
        qrid = resp['QRID'].encode()
        password ="jainjayakumar"
        cipher = b64decode(qrid)
        dqrid = decrypt(password, cipher)

        response = HttpResponse()
        try:
            conn = psycopg2.connect(database = "databasejson", user = "postgres", password = "raspberry", host = "127.0.0.1", port = "5432")
            response.write("\nOpened database successfully\n")
            cur = conn.cursor()
            cur.execute("SELECT * from PRODUCT WHERE QRID = '"+ str(dqrid.decode('utf-8'))+"';")
            rows = cur.fetchall()
            for row in rows:
                response.write("\nQRID = "+ row[0] +"\nSheetID = "+ row[1] + "\nBatchID = " + row[2] + "\nCompany = " + row[3] + "\nStatus = "+ str(row[4]))
            response.write("\n\nOperation done successfully")
        except (Exception, psycopg2.Error) as error :
            response.write("\nError while fetching data from PostgreSQL", error)
        finally:
	        #closing database connection.
	        if(conn):
	            cur.close()
	            conn.close()
	            response.write("\nPostgreSQL connection is closed")
        return response
    else:
        return HttpResponse('Please send a post http.')
@csrf_exempt
def qr_process(qrid):
    return HttpResponse(qrid)

