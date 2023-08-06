import morpfw
from dataclasses import dataclass, field
from datetime import date, datetime

import typing
import pytz

# {% if cookiecutter.project_type == "morpcc" %}
from morpcc.deform.referencewidget import ReferenceWidget
from morpcc.deform.vocabularywidget import VocabularyWidget
from morpcc.validator.reference import ReferenceValidator
from morpcc.validator.vocabulary import VocabularyValidator
# {% endif %}
from morpfw.validator.field import valid_identifier

@dataclass
class {{ cookiecutter.type_name }}Schema(morpfw.Schema):

    title: typing.Optional[str] = field(default=None, 
                                        metadata={'required': True})
    description: typing.Optional[str] = field(default=None,
                                        metadata={'format': 'text'})
