import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphene_django.filter import DjangoFilterConnectionField


class CityNode(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = ['city_name']
        interfaces = (graphene.relay.Node,)
class TitleNode(DjangoObjectType):
    class Meta:
        model = Title
        filter_fields = ['title_name']
        interfaces = (graphene.relay.Node,)
class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = [
              'employee_name',
              'employee_city__city_name',
              'employee_title__title_name'
               ]
        interfaces = (graphene.relay.Node,)
        
class CreateTitle(graphene.relay.ClientIDMutation):
    title = graphene.Field(TitleNode)
    class Input:
        title_name = graphene.String()
    def mutate_and_get_payload(root, info, **input):
        title = Title(
            title_name=input.get('title_name')
        )
        title.save()
        return CreateTitle(title=title)
    
class CreateEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode)
    class Input:
        employee_name = graphene.String()
        employee_city = graphene.String()
        employee_title = graphene.String()
        
    def mutate_and_get_payload(root, info, **input):
        employee = Employee(
           employee_name=input.get('employee_name'),
           employee_city=City.objects.get(
              city_name=input.get('employee_city')),
          employee_title=Title.objects.get(
             title_name=input.get('employee_title'))
        )
        employee.save()
        return CreateEmployee(employee=employee)
    

class Query(object):
    city = graphene.relay.Node.Field(CityNode)
    all_cities = DjangoFilterConnectionField(CityNode)
    title = graphene.relay.Node.Field(TitleNode)
    all_titles = DjangoFilterConnectionField(TitleNode)
    employee = graphene.relay.Node.Field(EmployeeNode)
    all_employees = DjangoFilterConnectionField(EmployeeNode)
    
class Mutation(graphene.ObjectType):
    create_title = CreateTitle.Field()
    create_employee = CreateEmployee.Field()