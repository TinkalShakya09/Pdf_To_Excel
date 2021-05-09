from django.shortcuts import render,HttpResponse
from .models import f3App
from PyPDF2 import PdfFileReader
import re
import pandas as pd
from collections import namedtuple
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
   
def index(request):
    global data
    global names
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        name=myfile.name
        names=name.replace('.pdf','.csv')
        names=str(names)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        path = fs.url(filename) 
        data=pdfToExcel(path)
        return render(request,'download.html')
    return render(request, 'index.html')

def pdfToExcel(path):
    global printdf    
    a=PdfFileReader(open( path, 'rb'))
    NumPages = a.getNumPages()
    Line = namedtuple('Line','Resaler_Name buyer_name Order_Number Quantity SKU COURIER_NAME AWB_NO Amount Buyer_Mobile_No Pincode HSN_Code')
    lines=[]
    regex_resaler_name = re.compile(r"BILL TO\s*(\w+ \w+ \w+),")
    regex_resaler_name1 = re.compile(r"BILL TO\s*(\w+ \w+),")
    regex_resaler_name2 = re.compile(r"BILL TO(\w+)")
    regex_buyer_name = re.compile(r"SHIP TO\s*(\w+ \w+ \w+)")
    regex_buyer_name1 = re.compile(r"SHIP TO\s*(\w+ \w+)")
    regex_buyer_name2 = re.compile(r"SHIP TO(\w+)")
    regex_order_id = re.compile(r"Order Number:\s*(\d+_\d)")
    regex_quantity =re.compile(r"Quantity:\s*(\d+)Color")
    regex_SKU = re.compile(r"SKU:\s*(\w+)Size")
    regex_SKU1 = re.compile(r"SKU:\s*(\w+-\w+-\w+)*Size")
    regex_SKU2 = re.compile(r"SKU:\s*(\w+ \w+)*Size")
    regex_courier_name = re.compile(r"(\Delhivery)")
    regex_courier_name1 = re.compile(r"\s*(\w+) Destination")
    regex_cin = re.compile(r"\s*(\d+)Fold")
    regex_amt = re.compile(r"Amount Rs.\s*(\d+)/-")
    regex_buyer_phone_no = re.compile(r"Mob No:\s*(\d+)")
    regex_pincode = re.compile(r"\s*(\w+)\s*Mob")
    regex_hsn_code =re.compile(r"Free Size \s*(\d+)Rs")

    for i in range(0,NumPages):
        str1=a.getPage(i).extractText()
        resaler_name = re.search(regex_resaler_name,str1)
        resaler_name1 = re.search(regex_resaler_name1,str1)
        resaler_name2 = re.search(regex_resaler_name2,str1)
        buyer_name = re.search(regex_buyer_name,str1)
        buyer_name1 = re.search(regex_buyer_name1,str1)
        buyer_name2 = re.search(regex_resaler_name2,str1)
        order_id = re.search(regex_order_id,str1)
        quantity = re.search(regex_quantity, str1)
        SKU = re.search(regex_SKU, str1)
        SKU1 = re.search(regex_SKU1,str1)
        SKU2 = re.search(regex_SKU2,str1)
        courier_name=re.search(regex_courier_name, str1)
        courier_name1=re.search(regex_courier_name1, str1)
        cin = re.search(regex_cin,str1)
        amt = re.search(regex_amt, str1)
        buyer_phone_no = re.search(regex_buyer_phone_no, str1)
        pincode = re.search(regex_pincode, str1)
        hsn_code = re.search(regex_hsn_code, str1)
        if resaler_name:
            resaler_name = resaler_name.group(1)
        elif resaler_name1:
            resaler_name =resaler_name1.group(1)
        elif resaler_name2:
            resaler_name =resaler_name2.group(1)
        if buyer_name:
            buyer_name = buyer_name.group(1)
        elif buyer_name1:
            buyer_name =buyer_name1.group(1)
        elif buyer_name2:
            buyer_name =buyer_name2.group(1)
        if order_id:
            order_id = order_id.group(1)
        if quantity:
            quantity = quantity.group(1)
        if SKU:
            SKU = SKU.group(1)
        elif SKU1:
            SKU = SKU1.group(1)
        elif SKU2:
            SKU = SKU2.group(1)
        if courier_name:
            courier_name = courier_name.group(1)
        elif courier_name1:
            courier_name =courier_name1.group(1)
        if cin:
            cin = cin.group(1)
        if amt:
            amt = amt.group(1)
        if buyer_phone_no:
            buyer_phone_no = buyer_phone_no.group(1)
        if pincode:
            pincode = pincode.group(1)
        if hsn_code:
            hsn_code = hsn_code.group(1)
        
        lines.append(Line(resaler_name,buyer_name, order_id, quantity, SKU,courier_name, cin, amt, buyer_phone_no, pincode, hsn_code))
        
    df = pd.DataFrame(lines)
    df = df.replace({"COURIER_NAME":{"Express":"Ecom Express", "Bees":"Xpress Bees"}})
    printdf = df.to_csv(index=False)
    return printdf

def download(request):
    global data
    global names
    index(request)
    response = HttpResponse(data,content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename='+names  
    return response   
