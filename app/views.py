import csv
from io import StringIO, BytesIO

import pandas
import xlsxwriter
import xlwt

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
# Create your views here.
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import CustomerForm
from .models import Customer
from xhtml2pdf import pisa

def home(request):
    data = Customer.objects.all()
    return  render(request, "datatable.html", {"data" : data})


class CustomerListView(SuccessMessageMixin, ListView):
  model = Customer
  template_name = 'home.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = CustomerForm
      return context


class CustomerCreateView(CreateView):
  form_class = CustomerForm
  template_name = 'customer_form.html'
  success_url = reverse_lazy('Home')


class CustomerUpdateView(UpdateView):
  model = Customer
  fields = "__all__"
  success_url = reverse_lazy('Home')
  success_message = 'Customer successfully updated.'
  template_name = 'update_form.html'



class CustomerDeleteView(DeleteView):
  model = Customer
  success_url = reverse_lazy('Home')
  template_name = 'home_delete.html'
  success_message = "The class {} has been deleted with all its attached content"

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class GenerateReport(View):
    def get(self, request, *args, **kwargs):
        min = request.GET.get("minage")
        max = request.GET.get("maxage")
        data = Customer.objects.filter(age__range=(min, max))
        if request.GET.get("filetype") == "pdf":
                template = get_template('report.html')
                context = {
                   "data" : data
                }
                html = template.render(context)
                pdf = render_to_pdf('report.html', context)
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Invoice_%s.pdf" %("12341231")
                    content = "inline; filename='%s'" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                return HttpResponse("Not found")

        elif request.GET.get("filetype") == "csv"  :

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
            writer = csv.writer(response)
            for i in data:
                writer.writerow([i.name, i.age, i.mobile_no])
            return response
        else:

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="users.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Name', 'Age', 'Mobile No']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            rows = Customer.objects.filter(age__range=(min, max)).values_list('name', 'age', 'mobile_no')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response

def graph(request):
    return  render(request, "graph.html")





