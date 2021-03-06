from marshmallow import ValidationError
from marshmallow import fields, validate, validates
from marshmallow_peewee import ModelSchema
from marshmallow_peewee import Related

from models import User, Project, Task


class UserSchema(ModelSchema):
    username = fields.Str(validate=[validate.Length(min=3, max=70)])
    password = fields.Str(validate=[validate.Length(min=3, max=30)])

    class Meta:
        model = User


class ProjectSchema(ModelSchema):
    name = fields.Str(validate=[validate.Length(min=3, max=100)])
    color = fields.Str(validate=[validate.Length(equal=7)])
    user = fields.Int()

    class Meta:
        model = Project

    @validates('user')
    def validate_user(self, user):
        if not User.filter(User.id == user).exists():
            raise ValidationError("Can't find user")


class TaskSchema(ModelSchema):
    name = fields.Str(validate=[validate.Length(min=3, max=100)])
    date = fields.Date()
    priority = fields.Int(validate=[validate.Range(min=1, max=3)])
    project = Related()

    class Meta:
        model = Task

    @validates('project')
    def validate_project(self, project):
        if not Project.filter(Project.id == project).exists():
            raise ValidationError("Can't find project")


user_schema = UserSchema()
project_schema = ProjectSchema()
task_schema = TaskSchema()
