import typing
from dataclasses import dataclass, field

import deform
import morepath
import morpfw
from inverter import dc2colander
from morpfw.crud.errors import ValidationError


class WizardStep(object):
    title: str = ""
    template: str
    index: int
    wizard: "Wizard"

    def __init__(self, context, request, wizard, index):
        self.context = context
        self.request = request
        self.wizard = wizard
        self.index = index

    def macro(self, load_template):
        return load_template(self.template).macros.step

    def handler_macro(self, load_template):
        return load_template(self.template).macros["step-handler"]

    def can_handle(self) -> bool:
        """
        check if the current form submission belong to this step, and
        return True if this step will handle the form processing
        """
        return False

    def finalize(self) -> bool:
        """
        this is run when wizard is finalized, check that all
        needed values are here
        """
        return True

    def completed(self) -> bool:
        return True

    @property
    def sessiondata(self):
        req = self.request
        req.session.setdefault("wizard_data", {})
        req.session["wizard_data"].setdefault(self.wizard.id, {})
        req.session["wizard_data"][self.wizard.id].setdefault("steps", {})
        data = req.session["wizard_data"][self.wizard.id]["steps"].get(self.index, None)
        return data

    @sessiondata.setter
    def sessiondata(self, data):
        req = self.request
        req.session.setdefault("wizard_data", {})
        req.session["wizard_data"].setdefault(self.wizard.id, {})
        req.session["wizard_data"][self.wizard.id].setdefault("steps", {})
        req.session["wizard_data"][self.wizard.id]["steps"][self.index] = data
        req.session.save()

    def clear_sessiondata(self):
        req = self.request
        req.session.setdefault("wizard_data", {})
        if self.sessiondata:
            del req.session["wizard_data"][self.wizard.id]["steps"][self.index]
            req.session.save()

    def handle(self):
        return {}


class FormWizardStep(WizardStep):

    template: str = "master/wizard/form-step.pt"
    schema: object

    def get_form(self, formid):
        formschema = dc2colander.convert(
            self.schema, request=self.request, default_tzinfo=self.request.timezone()
        )
        fs = formschema()
        fs = fs.bind(context=self.context, request=self.request)
        return deform.Form(fs, formid=formid)

    def can_handle(self):
        request = self.request
        formid = request.POST.get("__formid__")
        if formid:
            try:
                step = int(formid.split("-")[-1])
            except:
                return False

            if step == self.index:
                return True

        return False

    def process_form(self):
        request = self.request
        formschema = dc2colander.convert(
            self.schema, request=self.request, default_tzinfo=request.timezone()
        )
        fs = formschema()
        fs = fs.bind(context=self.context, request=self.request)
        controls = request.POST.items()
        form = deform.Form(fs, formid=request.POST.get("__formid__"))
        failed = False
        try:
            data = form.validate(controls)
        except deform.ValidationFailure as e:
            form = e
            failed = True
            data = controls

        if not failed:
            self.sessiondata = data

        return {"form": form, "failed": failed, "data": data}

    def completed(self):
        try:
            self.schema.validate(self.request, self.sessiondata)
        except ValidationError:
            return False
        return True

    def handle(self):
        result = self.process_form()

        # FIXME remember the value in session
        if result["failed"]:
            return {"step": self, "form": result["form"]}

        return {"step": self, "form": result["form"]}


class ConditionalBlockerWizardStep(WizardStep):

    template: str = "master/wizard/blocker-step.pt"

    def can_handle(self):
        request = self.request
        formid = request.POST.get("__formid__")
        if formid:
            try:
                step = int(formid.split("-")[-1])
            except:
                return False

            if step == self.index:
                return True

        return False

    def validate(self) -> bool:
        raise NotImplementedError

    def completed(self):
        if not self.validate():
            return False
        return True

    def handle(self):
        if not self.validate():
            return {"step": self, "error": True}

        return {"step": self, "error": False}


@dataclass
class AgreementForm(morpfw.BaseSchema):

    agree: bool = field(metadata={"deform": {"widget": deform.widget.CheckboxWidget()}})


class AgreementWizardStep(FormWizardStep):

    agreement_text: str
    agreement_checkbox_label: str
    agreement_error_msg: str

    template = "master/wizard/agreement-step.pt"
    schema = AgreementForm

    def completed(self):
        if not super().completed():
            return False

        if self.sessiondata.get("agree", False):
            return True

        return False

    def handle(self):
        result = self.process_form()
        data = result["data"]

        if result["failed"]:
            return {"step": self, "failed": True}

        if not data["agree"]:
            return {"step": self, "failed": True}

        return {"step": self, "failed": False}


class Wizard(object):
    steps: typing.List[WizardStep] = []
    style: str

    def __init__(self, context, request, identifier, style="horizontal"):
        self.id = identifier
        self.context = context
        self.style = style
        self.request = request
        steps = []
        for idx, step in enumerate(self.steps):
            s = step(context, request, self, idx)
            steps.append(s)
        self.steps = steps

    def macro(self, load_template, macro="wizard"):
        template = "master/wizard/wizard-macros.pt"
        return load_template(template).macros[macro]

    def finalize(self):
        self.clear()
        return morepath.redirect(self.request.link(self.context))

    def clear(self):
        del self.request.session["wizard_data"][self.id]
        self.request.session.save()

    def handle(self):
        request = self.request
        for step in self.steps:
            if step.can_handle():
                return step.handle()

        finalize_form = "%s-finalize" % self.id
        if request.POST.get("__formid__") == finalize_form:
            for step in self.steps:
                assert step.completed() == True
                step.finalize()

            return self.finalize()

        raise ValueError("Unable to process wizard form submission")
