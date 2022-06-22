from .data import data_const as data_content
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Reports, StatementOfFinancialPosition, StatementOfComprehensive
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .analysis.fin_analyst import Analysis


def convert_db_to_dict(data, const_text):
    data_db = [(k, v) for k, v in data.__dict__.items() if k not in ['id', 'report_id', '_state']]
    data_dict = {val_db[0]: {desc['name']: val_db[1], 'calculated': desc['calculated']}
                 for val_db, desc in zip(data_db, const_text)}
    return data_dict


def construct_reports(title, data_fields, val_space=2, id_title='_'):
    indent = ' '
    pattern = "^[0-9]*[.,]?[0-9]+$"
    template = [f'<h3 class="name-report">{title}</h3>', "<ul class = 'list-group'>", ]
    for key, val in data_fields.items():
        template.append(f"{indent*val_space}<li class='list-group-item'>")
        for k, v in val.items():
            if k != 'calculated':
                template.append(f"{indent*val_space*2}<label for='{id_title}_{key}'> {k}: </label>")
                template.append(f"{indent*val_space*2}<span> {float(v)} </span>")
        if val['calculated']:
            template.append('</li>')
        else:
            template.append(f'''{indent*val_space*2}<input placeholder="Change, only float" pattern={pattern}
            type="text" id="{id_title}_{ key }" name="{id_title}_{ key }"></li>''')
    template.append('</ul>')
    return '\n'.join(template)


def report_changes(post_data, title):
    parse_data = {}
    for k, v in post_data.items():
        key = k.split('_')
        if v and key[0] == title:
            try:
                value = float(v)
                parse_data[key[1]] = value
            except:
                return 'ValueTypeError'
    return parse_data


class StartPage(View):
    active = False
    user_companies = []

    def get(self, request):
        if request.user.is_authenticated:
            self.active = True
            companies = [obj.company for obj in Reports.objects.filter(user=request.user)]
            company_urls = [reverse('company', args=[request.user, company]) for company in companies]
            self.user_companies = [{'company': company, 'url': urls} for company, urls in zip(companies, company_urls)]

        context = {
            'name': request.user,
            'active': self.active,
            'companies': self.user_companies,
        }
        return render(request, 'AnalysisReport/start.html', context)

    def post(self, request):
        new_company = request.POST['company'].capitalize()
        if Reports.objects.filter(company=new_company, user=request.user):
            messages.error(request, 'Company is exists!!')
            return redirect('start')
        new_report = Reports(user=request.user, company=new_company)
        new_statement_financial_position = StatementOfFinancialPosition(report=new_report)
        new_statement_comprehensive = StatementOfComprehensive(report=new_report)
        new_report.save()
        new_statement_financial_position.save()
        new_statement_comprehensive.save()
        return redirect('start')


class RegisterUser(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('start')
        return render(request, 'AnalysisReport/register.html', {})

    def post(self, request):
        userName = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Passwords must be same')
            return redirect('register')
        else:
            user = User(username=userName, email=email, password=make_password(password))
            try:
                user.save()
                login(request, user)
                return redirect('start')
            except:
                messages.error(request, 'Password error!')
                return redirect('register')


class CompanyPage(View):

    def get(self, request, user, company):
        report_company = Reports.objects.filter(user=request.user, company=company)
        statement_financial_position = StatementOfFinancialPosition.objects.get(report__in=report_company)
        statement_of_comprehensive = StatementOfComprehensive.objects.get(report__in=report_company)

        sfp_dict = convert_db_to_dict(statement_financial_position, data_content.SFP_FIELDS)
        sc_dict = convert_db_to_dict(statement_of_comprehensive, data_content.SC_FIELDS)
        sfp_list = construct_reports('Statement of financial position', sfp_dict, id_title='sfp')
        sc_list = construct_reports('Statement of comprehensive', sc_dict, id_title='sc')
        context = {
            'user': user,
            'company': company,
            'sfp_list': sfp_list,
            'sc_list': sc_list
        }
        return render(request, 'AnalysisReport/data_company.html', context)

    def post(self, request, user, company):
        report_company = Reports.objects.filter(user=request.user, company=company)
        sfp_data = report_changes(request.POST, 'sfp')
        sc_data = report_changes(request.POST, 'sc')

        StatementOfFinancialPosition.objects.filter(report__in=report_company).update(**sfp_data)
        StatementOfComprehensive.objects.filter(report__in=report_company).update(**sc_data)
        return redirect(reverse('company', args=[user, company]))


class DeleteCompany(View):

    def get(self, request, user, company):
        report_company = Reports.objects.filter(user=request.user, company=company)
        report_company.delete()
        return redirect('start')


class CompanyFinAnPage(View):

    def get(self, request, user, company):
        report_company = Reports.objects.filter(user=request.user, company=company)
        sfp_data = StatementOfFinancialPosition.objects.get(report__in=report_company)
        sc_data = StatementOfComprehensive.objects.get(report__in=report_company)
        sfp_data = {k: v for k, v in sfp_data.__dict__.items() if k not in ['id', 'report_id', '_state']}
        sc_data = {k: v for k, v in sc_data.__dict__.items() if k not in ['id', 'report_id', '_state']}
        finance_ratios = Analysis(sfp_data, sc_data)
        print(finance_ratios.calculate())
        context = {
            'company': company,
            'ratios': finance_ratios.calculate()
        }
        return render(request, 'AnalysisReport/analysis.html', context)
