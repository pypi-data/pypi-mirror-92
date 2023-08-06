import morepath
from morpcc.wizard.wizard import Wizard, WizardStep, FormWizardStep
from morpcc.util import permits
from dataclasses import dataclass, field
from .app import App, AppRoot
from datetime import datetime
import deform.widget
from morpcc.deform.referencewidget import UserReferenceWidget


class Step1(WizardStep):

    title = 'Wizard Sample'
    description = 'This is a sample wizard'
    template = 'democms/wizard-step1.pt'


@dataclass
class Step2Form(object):

    text_data: str
    password_data: str = field(metadata={
        'deform': {
            'widget': deform.widget.PasswordWidget()
        }
    })
    datetime_data: datetime = field(metadata={
        'deform': {
            'widget': deform.widget.DateTimeInputWidget()
        }
    })
    user_reference: str = field(
        metadata={
            'deform': {
                'widget': UserReferenceWidget()
            }
        }
    )


@dataclass
class Step3Form(object):

    agree: bool = field(metadata={
        'deform': {
            'widget': deform.widget.CheckboxWidget()
        }
    })


class Step2(FormWizardStep):

    title = 'Sample Wizard Form'
    description = 'This view show an example of a wizard form'
    schema = Step2Form


class Step3(FormWizardStep):

    title = 'Final Wizard Form'
    description = 'This view show an example of a wizard form'
    schema = Step3Form
    template = 'democms/wizard-step3.pt'

    def handle(self):
        result = self.process_form()
        data = result['data']

        if result['failed']:
            return {'step': self,
                    'failed': True}

        if not data['agree']:
            return {'step': self,
                    'failed': True}

        return {'step': self,
                'failed': False}


class MyWizard(Wizard):

    steps = [Step1, Step2, Step3]


@App.html(model=AppRoot, name='wizard', template='master/wizard/wizard.pt')
def pagewizard(context, request):
    wizard = MyWizard(context, request, 'mywizard')
    return {
        'page_title': 'My Wizard',
        'wizard': wizard
    }


@App.html(model=AppRoot, name='wizard', template='master/wizard/process.pt',
          request_method='POST')
def pagewizard_process(context, request):
    wizard = MyWizard(context, request, 'mywizard')
    return wizard.handle()
