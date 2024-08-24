import graphene
from graphene_django import DjangoObjectType
from .models import *  # Import all models from the current module
from graphene_django.filter import DjangoFilterConnectionField  # For filtering query results
from graphql_relay.node.node import from_global_id  # Utility for decoding global IDs, used in updating

# Define a GraphQL node for the City model
class CityNode(DjangoObjectType):
    class Meta:
        model = City  # Specify the model to create the node from
        filter_fields = ['city_name']  # Allow filtering by city_name field
        interfaces = (graphene.relay.Node,)  # Use relay.Node interface

# Define a GraphQL node for the Title model
class TitleNode(DjangoObjectType):
    class Meta:
        model = Title  # Specify the model to create the node from
        filter_fields = ['title_name']  # Allow filtering by title_name field
        interfaces = (graphene.relay.Node,)  # Use relay.Node interface

# Define a GraphQL node for the Employee model
class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee  # Specify the model to create the node from
        filter_fields = [
            'employee_name',
            'employee_city__city_name',  # Allow filtering by related City model's city_name
            'employee_title__title_name'  # Allow filtering by related Title model's title_name
        ]
        interfaces = (graphene.relay.Node,)  # Use relay.Node interface

# Mutation to create a new Title
class CreateTitle(graphene.relay.ClientIDMutation):
    title = graphene.Field(TitleNode)  # Return the created TitleNode

    class Input:
        title_name = graphene.String()  # Input field for the title_name

    def mutate_and_get_payload(root, info, **input):
        title = Title(
            title_name=input.get('title_name')  # Create a new Title instance with the provided title_name
        )
        title.save()  # Save the new title to the database
        return CreateTitle(title=title)  # Return the created TitleNode

# Mutation to create a new Employee
class CreateEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode)  # Return the created EmployeeNode

    class Input:
        employee_name = graphene.String()  # Input field for the employee_name
        employee_city = graphene.String()  # Input field for the employee's city name
        employee_title = graphene.String()  # Input field for the employee's title name

    def mutate_and_get_payload(root, info, **input):
        # Create a new Employee instance with the provided input fields
        employee = Employee(
            employee_name=input.get('employee_name'),
            employee_city=City.objects.get(city_name=input.get('employee_city')),  # Retrieve the City instance
            employee_title=Title.objects.get(title_name=input.get('employee_title'))  # Retrieve the Title instance
        )
        employee.save()  # Save the new employee to the database
        return CreateEmployee(employee=employee)  # Return the created EmployeeNode

# Mutation to update an existing Employee
class UpdateEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode)  # Return the updated EmployeeNode

    class Input:
        id = graphene.String()  # Input field for the global ID of the employee
        employee_name = graphene.String()  # Input field for the new employee_name
        employee_city = graphene.String()  # Input field for the new employee_city name
        employee_title = graphene.String()  # Input field for the new employee_title name

    def mutate_and_get_payload(root, info, **input):
        # Retrieve the Employee instance using the global ID
        employee = Employee.objects.get(pk=from_global_id(input.get('id'))[1])
        # Update the employee's fields with the provided inputs
        employee.employee_name = input.get('employee_name')
        employee.employee_city = City.objects.get(city_name=input.get('employee_city'))  # Retrieve the City instance
        employee.employee_title = Title.objects.get(title_name=input.get('employee_title'))  # Retrieve the Title instance
        employee.save()  # Save the updated employee to the database
        return UpdateEmployee(employee=employee)  # Return the updated EmployeeNode

# Query class to define all available queries
class Query(object):
    city = graphene.relay.Node.Field(CityNode)  # Query to retrieve a single CityNode by ID
    all_cities = DjangoFilterConnectionField(CityNode)  # Query to retrieve all cities with filtering support
    title = graphene.relay.Node.Field(TitleNode)  # Query to retrieve a single TitleNode by ID
    all_titles = DjangoFilterConnectionField(TitleNode)  # Query to retrieve all titles with filtering support
    employee = graphene.relay.Node.Field(EmployeeNode)  # Query to retrieve a single EmployeeNode by ID
    all_employees = DjangoFilterConnectionField(EmployeeNode)  # Query to retrieve all employees with filtering support

# Mutation class to define all available mutations
class Mutation(graphene.ObjectType):
    create_title = CreateTitle.Field()  # Mutation to create a new title
    create_employee = CreateEmployee.Field()  # Mutation to create a new employee
    update_employee = UpdateEmployee.Field() # Mutation to update existing employee
